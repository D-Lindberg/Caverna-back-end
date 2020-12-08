    """ 
    Creates an Action Group Object which may or may not be nested. if it is not nested then it contains only the action name. if it is nested then it contains a list of actions that are to be separated by a common separator such as "and then / or" or "and / or" or "and then" or "either ... or".

    the object also contains methods that determine if an action is used, mark it as used, or set all actions as used or unused.
    """

class Action_Group:

    def __init__(self, action_name, is_single_action, order):
        self.actions = []
        self.action_name = action_name
        self.is_single_action = is_single_action
        self.order = order
        self.type = None
        self._is_used = False

    def __str__(self):
        if self.is_single_action:
            return self.action_name
        result = ""
        for index, sub_action_group in enumerate(self.actions):
            result += str(sub_action_group)
            if index < len(sub_action_group) - 1:
                result += self.type
        return result

    def get_is_used(self):
        if self.is_single_action:
            return self._is_used
        is_used = False
        for action_group in self.actions:
            if action_group.get_is_used():
                is_used = True
                break
        return is_used

    def set_is_used(self, boolean_value):
        if self.is_single_action:
            self._is_used = boolean_value
        else:
            for action_group in self.actions:
                action_group.set_is_used(boolean_value)

    def mark_action_as_used(self, action_name):
        if self.action_name == action_name:
            self.set_is_used(True)
        else:
            for action_group in self.actions:
                if action_group.is_single_action and not action_group.get_is_used():
                    action_group.mark_action_as_used(action_name)
                    if action_group.get_is_used():
                        return
                    else:
                        action_group.mark_action_as_used(action_name)
