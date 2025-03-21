// This file can be replaced during build by using the `fileReplacements` array.
// `ng build` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.

const homeFilePathUrl = 'HOMEFILEPATHURL'
const DicomFielPathUrl = 'DICOMFILEPATHURL'

export const environment = {
  production: false,

  imagePathurl:homeFilePathUrl,
  dicomPathUrl :DicomFielPathUrl,
  dicomUrl:"/v1/privacy/dicom/anonymize",

admin_fm_admin_get_OpenAiStatusandRoll : "/api/v1/rai/admin/getOpenAI",
admin_fm_admin_Update_OpenAiStatus : "/api/v1/rai/admin/UpdateOpenAI",
admin_fm_admin_UserRole : "/api/v1/rai/admin/userRole",
};

/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/plugins/zone-error';  // Included with Angular CLI.
