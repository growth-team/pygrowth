
class Extractor:

    def __init__(self):
        pass

    def validate_option_keys(self, options, acceptable_keys):
        for key in options.keys():
            if key not in acceptable_keys:
                raise ValueError(f"Key {key} is not accepted by this extractor")
