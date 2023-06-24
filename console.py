#!/usr/bin/python3

"""Module implements command line interface for manipulating objects"""

from models.base_model import BaseModel
from models.patients import Patient
from models.drugs import Drug
from models.payments import Payment
from models.users import User
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DB_Storage
import cmd
import models
from colorama import init, Fore, Back, Style

classes = {"Patient": Patient, "Drug": Drug, "Payment": Payment, "User": User}


class Console(cmd.Cmd):
    """Class Console implements command line interface"""
    prompt = Style.BRIGHT + Fore.GREEN + "HealthBridge>>> " + Style.RESET_ALL

    def do_quit(self, args):
        """Exits cmd interface"""
        print("Bye")
        print("Thank you for using HealthBridge")
        quit()

    def do_help(self, args):
        """renders help to user"""

    def preloop(self):
        print(Fore.LIGHTBLUE_EX + "\nHello and Welcome to HealthBridge" +
              Style.RESET_ALL + "  (default, March 12 2023, 08:01:47)")
        print("\nA user-friendly and comprehensive Hospital ", end="")
        print("Management System software solution that can ", end="")
        print("address the needs of hospitals and improve their operations\n")
        print("Version 1.0\n")

    def emptyline(self):
        """Continue to next prompt"""
        pass

    def do_all(self, args):
        """returns all objects in storage"""
        try:
            if len(args) == 0:
                all_objects = []
                for key, value in models.storage.all().items():
                    all_objects.append(str(value))
                print(all_objects)
                return
            arguments = args.split(" ")
            if len(arguments) == 1:
                class_objects = []
                if arguments[0] in classes:
                    for value in models.storage.all(arguments[0]).values():
                        class_objects.append(str(value))
                    print(class_objects)
                else:
                    print(Fore.RED + "Please enter a valid class"
                          + Style.RESET_ALL)
        except Exception:
            pass

    def do_create(self, args):
        """creates objects and saves them to storage"""
        try:
            if len(args) == 0:
                print("Please enter Class Name to create Object")
                return
            arguments = args.split(" ")

            if arguments[0] not in classes:
                print("**Invalid Class**")
                return

            if len(arguments) == 1:
                obj = eval(arguments[0])()
                obj.save()
                print(Fore.MAGENTA +
                      f"Successfully created {obj.__class__.__name__}"
                      +
                      f" object: id --  {obj.id}" + Style.RESET_ALL)
                return
            if len(arguments) > 1:
                new_dict = {}
                for entry in arguments[1:len(arguments)]:
                    key = entry.split("=")[0]
                    key = str(key)
                    key = key.replace('"', "")
                    key = key.replace("'", "")
                    attr = entry.split("=")[1]

                    if attr == "True" or attr == "False":
                        attr = bool(attr)
                    elif (attr[0] == '"'
                          and attr[len(attr) - 1] == '"' or
                          attr[0] == "'" and attr[len(attr) - 1] == "'"):
                        attr = str(attr)
                        attr = attr.replace('"', "")
                        attr = attr.replace("'", "")
                        attr = attr.replace("_", " ")
                    else:
                        try:
                            attr = int(attr)
                        except TypeError:
                            print("Not an integer")
                    new_dict.update({key: attr})
                obj = eval(arguments[0])(**new_dict)
                obj.save()
                print(f"Successfully Created {obj.__class__.__name__} object: "
                      + Fore.LIGHTGREEN_EX
                      + f" HealthBridge_id --  {obj.id}"
                      + Style.RESET_ALL)
        except Exception:
            pass

    def do_delete(self, args):
        """Deletes object from storage"""
        try:
            arguments = args.split(" ")
            if len(arguments) == 1:
                cid = args
                for key, value in models.storage.all().items():
                    obj_id = key.split(".")[1]
                    if cid == obj_id:
                        models.storage.delete(value)
                        print(Fore.RED + "Deleted" + Style.RESET_ALL)
        except Exception:
            pass

    def do_update(self, args):
        """Updates object"""
        try:
            arguments = args.split(" ")
            if len(arguments) > 1:
                new_dict = {}
                for entry in arguments[1:len(arguments)]:
                    key = entry.split("=")[0]
                    key = str(key)
                    key = key.replace('"', "")
                    key = key.replace("'", "")
                    attr = entry.split("=")[1]

                    if attr == "True" or attr == "False":
                        attr = bool(attr)
                    elif (attr[0] == '"' and attr[len(attr) - 1] == '"'
                          or attr[0] == "'" and attr[len(attr) - 1] == "'"):
                        attr = str(attr)
                        attr = attr.replace('"', "")
                        attr = attr.replace("'", "")
                        attr = attr.replace("_", " ")
                    else:
                        try:
                            attr = int(attr)
                        except TypeError:
                            print("Not an integer")
                    new_dict.update({key: attr})
                cid = arguments[0]
                for key in models.storage.all().keys():
                    obj_id = key.split(".")[1]
                    if cid == obj_id:
                        models.storage.update(key, **new_dict)
                        print(Fore.LIGHTMAGENTA_EX + "Instance Updated"
                              + Style.RESET_ALL)
        except Exception:
            pass

    def do_count(self, args):
        """Counts all objects"""
        try:
            if len(args) == 0:
                print("The total number of objects in Storage is {}".
                      format(len(models.storage.all())))
                return
            arguments = args.split(" ")
            if len(arguments) == 1:
                if arguments[0] in classes:
                    obj_count = len(models.storage.all(arguments[0]))
                    print("The total number of {}s in the HealthBridge "
                          + "Hospital Management System is ".
                          format(arguments[0]) + Fore.LIGHTGREEN_EX
                          + "{}".format(obj_count)
                          + Style.RESET_ALL)
                    return
                else:
                    print(Fore.RED + "Please enter a valid class" +
                          Style.RESET_ALL)
        except Exception:
            pass

    def do_show(self, args):
        """Prints object based id"""
        arguments = args.split(" ")
        try:
            if len(arguments) == 1:
                for key in models.storage.all().keys():
                    obj_id = key.split(".")[1]
                    if arguments[0] == obj_id:
                        class_name = key.split(".")[0]
                        print(models.storage.get(class_name, obj_id).to_dict())
        except Exception:
            pass


if __name__ == "__main__":
    Console().cmdloop()
