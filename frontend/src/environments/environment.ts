/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://fsndcaps.herokuapp.com/', // the running FLASK api server url
  auth0: {
    url: 'udacafe.eu', // the auth0 domain prefix
    audience: 'coffeeshop', // the audience set for the auth0 app
    clientId: 'Tgci7nSzOpfgtTPh9KbEimofvOVXauFP', // the client id generated for the auth0 app
    callbackURL: 'https://localhost:5000', // the base url of the running ionic application. 
  }
};
