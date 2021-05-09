from .linguaf import linguaf


# hide helper functions from user
for attribute in dir(linguaf):
    if callable(getattr(linguaf, attribute)):
        if not attribute.startswith("_"):
            globals()[attribute] = getattr(linguaf, attribute)
            