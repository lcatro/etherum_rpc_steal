
import platform
import threading


thread_output_lock = threading.Lock()
system_name = platform.architecture()[1].lower()

if 'windows' in system_name :
    import ctypes

    STD_INPUT_HANDLE = -10
    STD_OUTPUT_HANDLE= -11
    STD_ERROR_HANDLE = -12

    FOREGROUND_BLACK = 0x0
    FOREGROUND_BLUE = 0x01 # text color contains blue.
    FOREGROUND_GREEN= 0x02 # text color contains green.
    FOREGROUND_RED = 0x04 # text color contains red.
    FOREGROUND_INTENSITY = 0x08 # text color is intensified.

    BACKGROUND_BLUE = 0x10 # background color contains blue.
    BACKGROUND_GREEN= 0x20 # background color contains green.
    BACKGROUND_RED = 0x40 # background color contains red.
    BACKGROUND_INTENSITY = 0x80 # background color is intensified.

    class Color:

        std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

        def set_cmd_color(self, color, handle=std_out_handle):
            bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
            return bool

        def reset_color(self):
            self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

        def print_red_text(self, print_text):
            self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
            print(print_text)
            self.reset_color()

        def print_green_text(self, print_text):
            self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
            print(print_text)
            self.reset_color()

        def print_blue_text(self, print_text):
            self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
            print(print_text)
            self.reset_color()

        def print_red_text_with_blue_bg(self, print_text):
            self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY| BACKGROUND_BLUE | BACKGROUND_INTENSITY)
            print(print_text)
            self.reset_color()   

    color = Color()

    def red_output(text) :
        color.print_red_text(text)

    def green_output(text) :
        color.print_green_text(text)

    def bule_output(text) :
        color.print_blue_text(text)

    def red_text_bule_background_output(text) :
        color.print_red_text_with_blue_bg(text)

    def output_function(output_data,color = None) :
        thread_output_lock.acquire()

        if 'red' == color :
            red_output('%s' % output_data)
        elif 'green' == color :
            green_output('%s' % output_data)
        elif 'blue' == color :
            bule_output('%s' % output_data)
        else :
            print('%s' % output_data)

        thread_output_lock.release()
else :
    
    def output_function(output_data,color = None) :
        thread_output_lock.acquire()

        if 'red' == color :
            print('\033[31;1m%s\033[0m' % output_data)
        elif 'green' == color :
            print('\033[32;1m%s\033[0m' % output_data)
        elif 'bule' == color :
            print('\033[34;1m%s\033[0m' % output_data)
        else :
            print('%s' % output_data)

        thread_output_lock.release()
        
        
if __name__ == "__main__" :
    output_function('white')
    output_function('red','red')
    output_function('green','green')
    output_function('blue','blue')
     
