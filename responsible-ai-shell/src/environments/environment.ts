// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
// var url ="http://10.184.4.182" // goblal ip local
// var url ="http://10.68.120.107" // goblal ip local deepak chaange ip only in this to use this un comment line no 75 to 82 and comment 65 to  72
const url = 'ADMIN_URL' // goblal ip devlopemnt
// var batchUrl ="http://10.66.155.13" // goblal ip Pankaj


export const environment = {
  production: false,
  api:"http://dev.api.com",
  build_type:"dev",
  // master link for all ip and port no
  master_url:url+"/api/v1/rai/admin/ConfigApi",
  isSSO:'SSO_BASED_LOGIN'

};





