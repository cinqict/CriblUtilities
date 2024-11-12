**API Inputs**

This table shows the information sent with each field in the API Inputs call. 

| API Inputs field | db\_inputs.conf | db\_connections.conf | Fill in value |
| :---- | :---- | :---- | :---- |
| type |  |  | "collection" |
| schedule.cronSchedule | interval |  |  |
| schedule.run.mode | mode |  |  |
| schedule.enabled\* | disabled |  |  |
| collector.conf.connectionId | connection |  |  |
| collector.conf.query | query |  |  |
| collector.type |  |  | "database" |
| input.type |  |  | "collection" |
| input.metadata\[0\].name |  |  | “host” |
| input.metadata\[0\].value | host |  |  |
| input.metadata\[1\].value |  |  | “index” |
| input.metadata\[1\].value | index |  |  |
| input.metadata\[2\].value |  |  | “source” |
| input.metadata\[2\].value | source |  |  |
| input.metadata\[3\].value |  |  | “sourcetype” |
| input.metadata\[3\].value | sourcetype |  |  |
| id | \[....\]+unique code |  |  |

not sent values from inputs.conf:  
index\_time\_mode  
max\_rows

**API Connections**

| API Connections Field | db\_connections.conf | identities.conf |
| :---- | :---- | :---- |
| id | \[...\]+unique code  |  |
| databaseType | connection\_type\* |  |
| username |  | username |
| password |  | password |
| connectionString\* | customizedJdbcUrl |  |
| database | database |  |
| disabled | disabled |  |
| host | host |  |
| identity | identity |  |
| jdbcUseSSL | jdbcUseSSL |  |
| localTimezoneConversionEnabled | localTimezoneConversionEnabled |  |
| port | port |  |
| readonly |  | None |
| timezone |  | None |

## 

## schedule.enabled

Because Splunk talks about disabled and Cribl about enabled the states need to be transformed to the opposite value. Cribl only allows true or false booleans where Splunk allows 0 and 1 numbers as well; these need to be transformed.

| From | To |
| :---- | :---- |
| true | false |
| false | true |
| 1 | false |
| 0 | true |

## connection\_type

Cribl allowed values: mysql, oracle, postgres, sqlserver 

| From | To |
| :---- | :---- |
| oracle\_service | oracle |
| oracle | oracle |
| mssql\_jtds\_win\_auth | sqlserver |
| generic\_mssql | sqlserver |
| db2 | \-not supported yet- |
| postgres | postgres |
| sybase\_ase | \-not supported yet- |
| vertica | \-not supported yet- |

for \-not supported yet- throw an error.

## connectionString

If available this should be filled with customizedJdbcUrl contents. If not available this needs to be drafted using parameters (in curly brackets) available:  
jdbc:{connection\_type}://{host}:{post};encrypt={jdbcUseSSL};user={username};password={password};  
