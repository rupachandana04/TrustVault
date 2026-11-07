from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import FileResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect

def home(request):
    return HttpResponse("Welcome to TrustVault - Secure Document Sharing")

from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Document, DocumentPermission, AuditLog

def check_document_access(user, document, required_permission='read'):
    # Admin access
    if user.is_superuser:
        return True

    # Owner access
    if document.owner == user:
        return True

    # Check granted permission
    permission = DocumentPermission.objects.filter(
        document=document,
        user=user
    ).first()

    if not permission:
        return False

    # Edit permission also allows reading
    if required_permission == 'read':
        return permission.permission in ['read', 'edit']

    return permission.permission == 'edit'

# Create your views here.
def create_audit_log(user, document, action, details=''):
    AuditLog.objects.create(
        user=user,
        document_title=document.title,
        action=action,
        details=details
        
    
    )
    
@login_required
def upload_document(request):
    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        category = request.POST.get('category', '').strip()
        uploaded_file = request.FILES.get('file')

        if not title or not uploaded_file:
            return HttpResponse("Title and file are required.")

        if len(title) > 200:
            return HttpResponse("Title is too long.")

        # File type validation
        allowed_extensions = ['pdf', 'docx', 'txt']
        extension = uploaded_file.name.rsplit('.', 1)[-1].lower()

        if '.' not in uploaded_file.name or extension not in allowed_extensions:
            return HttpResponse("Invalid file type.")

        # File size validation (5 MB)
        if uploaded_file.size > 5 * 1024 * 1024:
            return HttpResponse("File size must be below 5 MB.")

        document = Document.objects.create(
            title=title,
            category=category,
            file=uploaded_file,
            owner=request.user
        )

        create_audit_log(
            request.user,
            document,
            'upload',
            'Document uploaded successfully'
        )

        return HttpResponse("Document uploaded successfully!")

    return render(request, 'documents/upload.html')

@login_required
def download_document(request, document_id):

    document = get_object_or_404(
        Document,
        id=document_id
    )

    # Check read permission
    if not check_document_access(
        request.user,
        document,
        'read'
    ):
        return HttpResponseForbidden(
            "You don't have permission to download this document."
        )

    # Create audit log
    create_audit_log(
        request.user,
        document,
        'download',
        'Document downloaded successfully'
    )

    # Send file
    return FileResponse(
        document.file.open('rb'),
        as_attachment=True,
        filename=document.file.name.split('/')[-1]
    )
    
    
@login_required
def document_list(request):
    documents = Document.objects.filter(owner=request.user)

    return render(
        request,
        'documents/document_list.html',
        {'documents': documents}
    )
    
@login_required
def share_document(request, document_id):

    document = get_object_or_404(
        Document,
        id=document_id,
        owner=request.user
    )

    if request.method == 'POST':

        username = request.POST.get('username')
        permission_type = request.POST.get('permission')

        if permission_type not in ['read', 'edit']:
            return HttpResponse("Invalid permission.")

        user = get_object_or_404(
            User,
            username=username
        )

        if user == request.user:
            return HttpResponse("You cannot share with yourself.")

        DocumentPermission.objects.update_or_create(
            document=document,
            user=user,
            defaults={'permission': permission_type}
        )

        create_audit_log(
            request.user,
            document,
            'permission_granted',
            f'{permission_type} permission granted to {username}'
        )

        return HttpResponse("Document shared successfully!")

    return render(
        request,
        'documents/share_document.html',
        {'document': document}
    )
    
@login_required
def shared_documents(request):

    permissions = DocumentPermission.objects.filter(
        user=request.user
    ).select_related('document', 'document__owner')

    return render(
        request,
        'documents/shared_documents.html',
        {'permissions': permissions}
    )