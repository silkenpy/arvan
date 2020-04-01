# arvan
Arvan is python api to work with arvancloud (ابر آروان)

This api is based arvancloud doc which provided on 
https://napi.arvancloud.com/docs/iaas/1.0#/

from arvan.client import Client

arv = Client("Apikey 22222222-5555-bbbb-aaaa-6f3a99e60e76")
print(arv.get_region())
print(arv.all_images)
print(arv.get_all_regions())
print(arv.get_region_servers())
print(arv.get_region_images('nl-ams-su1'))
print(arv.get_region_networks())
print(arv.get_region_sizes())
print(arv.get_region_networks("nl-ams-su1"))
print(arv.get_region_security_group("ir-thr-mn1"))
print(arv.get_region_ssh_keys())
print(arv.create(name="mytest", ssh_key_name="no", count=1))
print(arv.get_region_servers())
print(arv.delete(vm_id="6e71f738-cc77-46aa-b604-eb966e66da72"))
print(arv.delete_all("ir-thr-at1", "mytest"))
print(arv.delete_list(vm_list=["094f0ee9-bf99-4214-acc6-46072d568752"]))
print(arv.delete(vm_id="6e008780-3a89-4730-ab5f-a7a94e929db1"))
