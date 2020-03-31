from django.http import HttpResponse,Http404,HttpResponseRedirect
from  django.template import loader
from .models import Question,Choice
from  django.shortcuts import render,get_object_or_404
from  django.urls import  reverse
from  django.views import generic

from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #Question.objects.filter(pub_date__lte=timezone.now()) r返回一个查询集,包括pub_date 小于或者等于timezone.now的Question
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list':latest_question_list
    # }
    #
#    return  HttpResponse(template.render(context,requset))
#升级后
    # return render(requset,'polls/index.html',context)
#    output = ','.join([q.question_text for q in latest_question_list])
 #   return  HttpResponse(output)

# def detail(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return  render(request,'polls/detail.html',{'question':question})
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exits")
    #
    # return render(request,'polls/detail.html',{'question':question_id})
#    return HttpResponse("You're looking at question %s."% question_id)


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #重定向 ：HttpResponseRedirect   reverse：反解析
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))