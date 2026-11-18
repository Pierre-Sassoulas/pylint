class OptionType(graphene.InputObjectType):
    freeform_enabled = graphene.Boolean(required=True)
    freeform_enabled = GenericScalar(required=True)
