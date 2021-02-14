/* @TODO DONE replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-ly1s0q43.eu', // the auth0 domain prefix
    audience: '127.0.0.1', // the audience set for the auth0 app
    clientId: 'QNBNuclSEF2yjc5oalEmNb57yo0bylQ7', // the client id generated for the auth0 app # QNBNuclSEF2yjc5oalEmNb57yo0bylQ7
    callbackURL: 'https://127.0.0.1:8100', // the base url of the running ionic application.
  }
};
