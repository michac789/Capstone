from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(request, posts, num):
    p = Paginator(posts, num)
    if "page" in request.GET:
        try:
            output_page = p.page(request.GET["page"])
        except PageNotAnInteger:
            return p.page(1)
        except EmptyPage:
            try:
                output_page = p.page(int(request.GET["page"]) - 1)
            except EmptyPage:
                output_page = p.page(1)
        return output_page
    else: return p.page(1)


def getcount(posts, start=1):
    for (i, post) in enumerate(posts):
        newpost = post
        newpost.count = i + start
    return posts


# temp = gamesession.game.get_questiontype1_order()
# print(x)
# print(x[0])
# print(x[1])
# print(x[2])
# print(type(x[1]))

# question = QuestionType1.objects.get(id=temp[gamesession.current_question])
# print(question.question)
# print(gamesession.current_question)
# print(gamesession.serialize())
