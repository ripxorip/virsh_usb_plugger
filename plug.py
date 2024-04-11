import argparse
import os

def get_vendor_and_product_id(device):
    if device == "headphones":
        return "0x046d", "0x0aba"
    elif device == "gamepad":
        return "0x045e", "0x028e"
    elif device == "spacemouse":
        return "0x256f", "0xc652"
    elif device == "spacemouse_wired":
        return "0x256f", "0xc62e"
    elif device == "spacemouse_enterprise":
        return "0x256f", "0xc633"
    else:
        return None, None

def write_xml_file(vendor_id, product_id):
    # Get the path of the current python file
    path = os.path.dirname(os.path.abspath(__file__))
    # Write the xml file in the same directory
    with open(f'{path}/usb.xml', 'w') as f:
        f.write(f"""
        <hostdev mode='subsystem' type='usb' managed='yes'>
            <source>
                <vendor id='{vendor_id}'/>
                <product id='{product_id}'/>
            </source>
        </hostdev>""")
    return path

def plug(device, vm):
    vendor_id, product_id = get_vendor_and_product_id(device)
    if vendor_id is None or product_id is None:
        print(f'No vendor_id and product_id found for {device}')
        return
    path = write_xml_file(vendor_id, product_id)
    os.system(f'sudo virsh attach-device {vm} --file {path}/usb.xml --current')

def unplug(device, vm):
    vendor_id, product_id = get_vendor_and_product_id(device)
    if vendor_id is None or product_id is None:
        print(f'No vendor_id and product_id found for {device}')
        return
    path = write_xml_file(vendor_id, product_id)
    os.system(f'sudo virsh detach-device {vm} --file {path}/usb.xml --current')


def main(device, action, vm):
    if action == 'plug':
        plug(device, vm)
    elif action == 'unplug':
        unplug(device, vm)
    else:
        print(f'Action {action} not supported')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--device", required=True, help="Device to be controlled")
    parser.add_argument("-a", "--action", required=True, choices=['plug', 'unplug'], help="Action to be performed on the device")
    parser.add_argument("-v", "--vm", required=True, help="Virtual machine where the action is performed")
    args = parser.parse_args()

    main(args.device, args.action, args.vm)
