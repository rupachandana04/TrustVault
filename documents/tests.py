import tempfile

from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Document, DocumentPermission, AuditLog
from .views import check_document_access


class TrustVaultSecurityTests(TestCase):

    def setUp(self):
        self.temp_media = tempfile.TemporaryDirectory()
        self.settings_override = override_settings(
            MEDIA_ROOT=self.temp_media.name
        )
        self.settings_override.enable()

        self.addCleanup(self.settings_override.disable)
        self.addCleanup(self.temp_media.cleanup)

        self.owner = User.objects.create_user(
            username='owner',
            password='testpass123'
        )

        self.other_user = User.objects.create_user(
            username='other',
            password='testpass123'
        )

        self.document = Document.objects.create(
            title='Test Document',
            owner=self.owner,
            category='Testing',
            file=SimpleUploadedFile(
                'test.pdf',
                b'%PDF-1.4 Test content',
                content_type='application/pdf'
            )
        )

    # 1. Login protection
    def test_upload_requires_login(self):
        response = self.client.get(
            reverse('upload_document')
        )

        self.assertEqual(response.status_code, 302)

    # 2. Document owner can download
    def test_owner_can_download_document(self):
        self.client.login(
            username='owner',
            password='testpass123'
        )

        response = self.client.get(
            reverse(
                'download_document',
                args=[self.document.id]
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)

        self.assertTrue(
            AuditLog.objects.filter(
                action='download',
                user=self.owner
            ).exists()
        )

        response.close()

    # 3. Unauthorized user cannot download
    def test_unauthorized_user_cannot_download(self):
        self.client.login(
            username='other',
            password='testpass123'
        )

        response = self.client.get(
            reverse(
                'download_document',
                args=[self.document.id]
            )
        )

        self.assertEqual(response.status_code, 403)

    # 4. Read permission allows download
    def test_read_permission_allows_download(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.other_user,
            permission='read'
        )

        self.client.login(
            username='other',
            password='testpass123'
        )

        response = self.client.get(
            reverse(
                'download_document',
                args=[self.document.id]
            )
        )

        self.assertEqual(response.status_code, 200)
        response.close()

    # 5. Edit permission also allows reading
    def test_edit_permission_allows_read_access(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.other_user,
            permission='edit'
        )

        result = check_document_access(
            self.other_user,
            self.document,
            'read'
        )

        self.assertTrue(result)

    # 6. Read permission does not allow editing
    def test_read_permission_does_not_allow_edit_access(self):
        DocumentPermission.objects.create(
            document=self.document,
            user=self.other_user,
            permission='read'
        )

        result = check_document_access(
            self.other_user,
            self.document,
            'edit'
        )

        self.assertFalse(result)

    # 7. Invalid file extension rejected
    def test_invalid_file_extension_rejected(self):
        self.client.login(
            username='owner',
            password='testpass123'
        )

        uploaded_file = SimpleUploadedFile(
            'virus.exe',
            b'test content'
        )

        response = self.client.post(
            reverse('upload_document'),
            {
                'title': 'Invalid File',
                'category': 'Testing',
                'file': uploaded_file
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid file type.')
        self.assertFalse(
            Document.objects.filter(title='Invalid File').exists()
        )

    # 8. Files above 5 MB rejected
    def test_large_file_rejected(self):
        self.client.login(
            username='owner',
            password='testpass123'
        )

        uploaded_file = SimpleUploadedFile(
            'large.pdf',
            b'A' * (5 * 1024 * 1024 + 1)
        )

        response = self.client.post(
            reverse('upload_document'),
            {
                'title': 'Large File',
                'file': uploaded_file
            }
        )

        self.assertContains(
            response,
            'File size must be below 5 MB.'
        )

        self.assertFalse(
            Document.objects.filter(title='Large File').exists()
        )

    # 9. Successful upload creates audit log
    def test_successful_upload_creates_audit_log(self):
        self.client.login(
            username='owner',
            password='testpass123'
        )

        uploaded_file = SimpleUploadedFile(
            'new.pdf',
            b'%PDF-1.4 New document'
        )

        response = self.client.post(
            reverse('upload_document'),
            {
                'title': 'New Document',
                'category': 'Testing',
                'file': uploaded_file
            }
        )

        self.assertContains(
            response,
            'Document uploaded successfully!'
        )

        self.assertTrue(
            AuditLog.objects.filter(
                document_title='New Document',
                action='upload',
                user=self.owner
            ).exists()
        )

    # 10. User cannot share another person's document
    def test_non_owner_cannot_share_document(self):
        self.client.login(
            username='other',
            password='testpass123'
        )

        response = self.client.get(
            reverse(
                'share_document',
                args=[self.document.id]
            )
        )

        self.assertEqual(response.status_code, 404)