from django.shortcuts import render , HttpResponse
import os
import pdfplumber # type: ignore
import docx # type: ignore
from django.shortcuts import render
from .forms import DocumentForm

from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags


from transformers import BartTokenizer, BartForConditionalGeneration
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

# Create your views here.


@csrf_exempt
def summarize_text(request):
    summary = ''
    original = ''
    if request.method == 'POST':
        original = request.POST.get('content', '')
        if original:
            # Clean + Limit length to avoid token limit (1024 for BART)
            original = strip_tags(original)[:3000]

            inputs = tokenizer.encode(original, return_tensors='pt', max_length=1024, truncation=True)
            summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return render(request, 'base/summary.html', {
        'summary': summary,
        'original': original
    })

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return '\n'.join(page.extract_text() or '' for page in pdf.pages)

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return '\n'.join([para.text for para in doc.paragraphs])

def index(request):
    text = ''
    file_info = {}
    form = DocumentForm()

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            file_path = doc.file.path
            ext = os.path.splitext(file_path)[1].lower()

            if ext == '.pdf':
                text = extract_text_from_pdf(file_path)
            elif ext == '.docx':
                text = extract_text_from_docx(file_path)
            else:
                text = 'Unsupported file format.'

            file_info = {
                'name': os.path.basename(file_path),
                'size': round(os.path.getsize(file_path) / 1024, 2)
            }

    return render(request, 'base/home.html', {
        'form': form,
        'text': text,
        'file_info': file_info
    })


def download_summary(request):
    summary = request.GET.get('summary', '')
    response = HttpResponse(summary, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="summary.txt"'
    return response