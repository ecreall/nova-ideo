import graphene


class Upload(graphene.InputObjectType):
    name = graphene.String()
    type = graphene.String()
    uri = graphene.String()
