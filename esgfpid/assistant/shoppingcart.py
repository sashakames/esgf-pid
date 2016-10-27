import logging
import esgfpid.utils
import esgfpid.assistant.messages
from esgfpid.utils import loginfo, logdebug, logtrace, logerror, logwarn

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

class ShoppingCartAssistant(object):

    def __init__(self, **args):
        mandatory_args = ['prefix', 'coupler']
        esgfpid.utils.check_presence_of_mandatory_args(args, mandatory_args)
        esgfpid.utils.check_noneness_of_mandatory_args(args, mandatory_args)
        self.__prefix = args['prefix']
        self.__coupler = args['coupler']

    def make_shopping_cart_pid(self, list_of_drs_ids):
        logdebug(LOGGER, 'Making a PID for a shopping cart full of datasets...')

        # Make a pid (hash on the content):
        list_of_drs_ids = self.__get_strings_as_list(list_of_drs_ids)
        cart_handle = self.__get_handle_for_cart(list_of_drs_ids, self.__prefix)

        # Make and send message
        message = self.__make_message(cart_handle, list_of_drs_ids)
        self.__send_message_to_queue(message)

        # Return pid
        logdebug(LOGGER, 'Making a PID for a shopping cart full of datasets... done.')
        loginfo(LOGGER, 'Requesting to create PID for data cart (%s).', cart_handle)
        return cart_handle

    def __get_strings_as_list(self, strings):
        if type(strings) == type([]):
            return strings
        else:
            return [strings]

    def __get_handle_for_cart(self, list_of_drs_ids, prefix):
        hash_basis = esgfpid.utils.make_sorted_lowercase_list_without_hdl(list_of_drs_ids)
        return esgfpid.utils.make_handle_from_list_of_strings(hash_basis, prefix)
        # This sorts the list, removes all "hdl:", and makes a hash

    def __make_message(self, cart_handle, data_cart_content):
        message_timestamp = esgfpid.utils.get_now_utc_as_formatted_string()
        message = esgfpid.assistant.messages.make_shopping_cart_message(
            cart_handle = cart_handle,
            timestamp = message_timestamp,
            data_cart_content = data_cart_content
        )
        return message

    def __send_message_to_queue(self, message):
        self.__coupler.send_message_to_queue(message)