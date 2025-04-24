from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'base/index.html')
def summarize_text(request):
    if request.method == 'POST':
        # text = request.POST.get('text')
        # Here you would call your summarization function
        summary = "This is a dummy summary."  # Replace with actual summarization logic
        return render(request, 'summarizer/index.html', {'summary': summary})
    return render(request, 'base/index.html')