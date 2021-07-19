# ledkovac-server

## how to run
* docker-compose build
* docker-compose up -d

#### ledkovac server 
* localhost:5600 
#### kibana
* localhost:5601

## first setup in Kibana
* open kibana
* select `stack management` on the left side
* `saved objects`
* `import`
* select the `kibana.ndjson` file located in this project and import it. New dashboard will be added. 

## linux system settings
* add permissions to the data folder (create the data01 folder if it doesn't exist yet in the server folder)
    * sudo chmod 777 -R data01/
* set `vm.max_map_count` in `/etc/sysctl.conf`
    * vm.max_map_count=262144

