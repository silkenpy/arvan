import json
import requests
from time import time

base_url = "https://napi.arvancloud.com/ecc/v1/regions"


def api_key_validator(api_key, region="ir-thr-at1"):
    len_api_key = len(api_key)
    if len_api_key == 36:
        key = api_key
    elif len_api_key == 43:
        key = api_key.split(" ")[1]
    else:
        return False
    res = requests.get("%s/%s/servers" % (base_url, region), headers={"Authorization": "Apikey %s" % key})
    if res.status_code == 200:
        return True
    else:
        print(res.status_code)
        print("This Apikey is not usable at this time !")
        raise Exception


class Client:
    def __init__(self, api_key, region="ir-thr-at1", printing=True):
        api_key_validator(api_key, region)
        self.api_key = api_key
        self.region = region
        self.all_regions = ["ir-thr-mn1", "ir-thr-at1", "nl-ams-su1"]
        self.all_images = {}
        self.get_region_images()
        self.all_networks = {}
        self.get_region_networks()
        self.all_sizes = {}
        self.get_region_sizes()
        self.all_security_group = {}
        self.get_region_security_group()
        self.all_ssh_keys = {}
        self.get_region_ssh_keys()
        self.all_servers = {}

        if printing:
            for i in [self.region, self.all_images, self.all_networks, self.all_sizes, self.all_security_group,
                      self.all_ssh_keys, self.all_servers]:
                print(i)

    def set_default_region(self, region):
        api_key_validator(self.api_key, region)
        self.region = region

    def set_available_regions(self, regions):
        self.all_regions = regions

    def get_all_regions(self):
        return self.all_regions

    def get_region(self):
        return self.region

    def get_all_region_servers(self):
        for region in self.all_regions:
            self.get_region_servers(region)
        return self.all_servers

    def get_region_servers(self, region=""):
        if not region:
            region = self.region

        res = requests.get("%s/%s/servers" % (base_url, region), headers={"Authorization": "Apikey %s" % self.api_key})
        if res.status_code == 200:
            result = {}
            for n in json.loads(res.content)['data']:
                result[n["name"]] = {}
                result[n["name"]]["id"] = n["id"]
                result[n["name"]]["addr"] = ""
                if "public1" in n["addresses"]:
                    result[n["name"]]["addr"] = n["addresses"]["public1"][0]["addr"]
                result[n["name"]]["status"] = n["status"]
                result[n["name"]]["plan"] = {"id": n["flavor"]["id"], "disk": n["flavor"]["disk"],
                                             "memory": n["flavor"]["ram"], "cpu": n["flavor"]["vcpus"]}

            self.all_servers[region] = result
            return self.all_servers[region]
        else:
            raise Exception

    def get_region_images(self, region="", img_type="distributions"):
        if not region:
            region = self.region

        res = requests.get("%s/%s/images?type=%s" % (base_url, region, img_type),
                           headers={"Authorization": "Apikey %s" % self.api_key})
        if res.status_code == 200:
            result = {}
            for n in json.loads(res.content)['data']:
                result[n["name"]] = {}
                for img in n["images"]:
                    version = img["name"]
                    result[n["name"]][version] = img["id"]
            self.all_images[region] = result
            return self.all_images
        else:
            raise Exception

    def get_region_networks(self, region=""):
        if not region:
            region = self.region

        res = requests.get("%s/%s/networks" % (base_url, region),
                           headers={"Authorization": "Apikey %s" % self.api_key})
        if res.status_code == 200:
            result = []
            for n in json.loads(res.content)['data']:
                result.append(n["id"])
            self.all_networks[region] = result
            return self.all_networks
        else:
            raise Exception

    def get_region_sizes(self, region=""):
        if not region:
            region = self.region

        res = requests.get("%s/%s/sizes" % (base_url, region), headers={"Authorization": "Apikey %s" % self.api_key})
        if res.status_code == 200:
            result = {}
            for plan in json.loads(res.content)['data']:
                result[plan["name"]] = {"order": plan["order"], "memory": plan["memory"], "cpu": plan["cpu_count"],
                                        "disk": plan["disk"]}
            self.all_sizes[region] = result
            return self.all_sizes
        else:
            raise Exception

    def get_region_security_group(self, region=""):
        if not region:
            region = self.region

        res = requests.get("%s/%s/securities" % (base_url, region),
                           headers={"Authorization": "Apikey %s" % self.api_key})
        if res.status_code == 200:
            result = {}
            for n in json.loads(res.content)['data']:
                result[n["name"]] = n["id"]
            self.all_security_group[region] = result
            return self.all_security_group
        else:
            raise Exception

    def get_region_ssh_keys(self, region=""):
        if not region:
            region = self.region

        res = requests.get("%s/%s/ssh-keys" % (base_url, region), headers={"Authorization": "Apikey %s" % self.api_key})
        if res.status_code == 200:
            result = []
            for n in json.loads(res.content)['data']:
                result.append(n["name"])
            self.all_ssh_keys[region] = result
            return self.all_ssh_keys
        else:
            raise Exception

    def create(self, name="", region="", image="", network="", flavor="", ssh_key=True, ssh_key_name=0,
               security_group="", count=1):
        if not name:
            name = str(int(time()))
        if not region:
            region = self.region
        if not image:
            image = self.all_images[region]['ubuntu']['18.04']
        if not network:
            network = self.all_networks[region][0]
        if not flavor:
            flavor = self.all_sizes[region]['standard1']['order']
        if not security_group:
            security_group = self.all_security_group[region]['default']

        res = requests.post("%s/%s/servers" % (base_url, region),
                            headers={"Authorization": "Apikey %s" % self.api_key, 'Connection': 'keep-alive',
                                     'Accept': '*/*', 'Accept-Language': 'fa', 'content-encoding': 'gzip',
                                     'Content-Type': 'application/json;charset=utf-8'
                                     },
                            data=json.dumps(
                                {"image_id": image, "flavor_id": flavor, "name": name, "key_name": ssh_key_name,
                                 "network_id": network, "security_groups": [{"name": security_group}],
                                 "ssh_key": ssh_key, "count": count}),
                            )
        if res.status_code == 201:
            return True
        else:
            return False

    def delete(self, vm_id, region=""):
        if not vm_id:
            return False
        if not region:
            region = self.region
        res = requests.delete("%s/%s/servers/%s" % (base_url, region, vm_id),
                              headers={"Authorization": "Apikey %s" % self.api_key})
        if res.status_code == 200:
            return True
        return False

    def delete_cluster(self, vm_name, region=""):
        result = True
        if not region:
            region = self.region
        self.get_region_servers(region)
        for name in self.all_servers[region]:
            if name.startswith(vm_name + "-"):
                result *= self.delete(self.all_servers[region][name]["id"], region)
            else:
                result = False
        return result

    def delete_list(self, vm_list, region=""):
        result = True
        if not region:
            region = self.region
        for vm in vm_list:
            result *= self.delete(vm, region)
        return result

    def power_off(self, vm_id, region=""):
        if not vm_id:
            return False
        if not region:
            region = self.region
        res = requests.post("%s/%s/servers/%s/power-off" % (base_url, region, vm_id),
                            headers={"Authorization": "Apikey %s" % self.api_key})
        if res.status_code == 202:
            return True
        return False

    def power_off_cluster(self, vm_name, region=""):
        result = True
        if not region:
            region = self.region
        self.get_region_servers(region)
        for name in self.all_servers[region]:
            if name.startswith(vm_name + "-"):
                result *= self.power_off(self.all_servers[region][name]["id"], region)
        return result

    def power_off_list(self, vm_list, region=""):
        result = True
        if not region:
            region = self.region
        for vm in vm_list:
            result *= self.power_off(vm, region)
        return result

    def power_on(self, vm_id, region=""):
        if not vm_id:
            return False
        if not region:
            region = self.region
        res = requests.post("%s/%s/servers/%s/power-on" % (base_url, region, vm_id),
                            headers={"Authorization": "Apikey %s" % self.api_key})
        if res.status_code == 202:
            return True
        return False

    def power_on_cluster(self, vm_name, region=""):
        result = True
        if not region:
            region = self.region
        self.get_region_servers(region)
        for name in self.all_servers[region]:
            if name.startswith(vm_name + "-"):
                result *= self.power_on(self.all_servers[region][name]["id"], region)
        return result

    def power_on_list(self, vm_list, region=""):
        result = True
        if not region:
            region = self.region
        for vm in vm_list:
            result *= self.power_on(vm, region)
        return result

    def get_cluster_servers(self, vm_name, region=""):
        result = {}
        if not region:
            region = self.region
        for name in self.all_servers[region]:
            if name.startswith(vm_name + "-"):
                result[name] = self.all_servers[region][name]
        return result

    def get_list_of(self, variable_name, region="", node=""):
        if not region:
            region = self.region
        return list(filter(lambda x: x, [self.all_servers[region][vm][variable_name] if (node in vm) else None for vm in
                                         self.all_servers[region]]))
