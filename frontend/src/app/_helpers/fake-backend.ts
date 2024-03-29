﻿import {Injectable} from '@angular/core';
import {HTTP_INTERCEPTORS, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest, HttpResponse} from '@angular/common/http';
import {Observable, of, throwError} from 'rxjs';
import {delay, dematerialize, materialize} from 'rxjs/operators';

// array in local storage for registered users
const usersKey = 'angular-10-registration-login-example-users';
let users = JSON.parse(localStorage.getItem(usersKey)) || [];

@Injectable()
export class FakeBackendInterceptor implements HttpInterceptor {
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const {url, method, headers, body} = request;

    return handleRoute();

    function currentTrend() {
      const tags = request.params.getAll('tags')
      console.log(tags)
      return ok({
        '2009': {'posts': 0.1674608107},
        '2010': {'posts': 0.0575115315},
        '2011': {'posts': 0.0606754039},
        '2012': {'posts': 0.0700105729},
        '2013': {'posts': 0.089297846},
        '2014': {'posts': 0.1011863872},
        '2015': {'posts': 0.1319705512},
        '2016': {'posts': 0.1590640688},
        '2017': {'posts': 0.1719779959},
        '2018': {'posts': 0.1598052794},
        '2019': {'posts': 0.1525956232},
        '2020': {'posts': 0.1224838084}
      })
    }

    function getTags() {
      return ok(['Laravel'
        , 'Codeigniter'
        , 'React'
        , 'PHP'
        , 'Python'
        , 'Vue'
        , 'JQuery'
        , 'Javascript']
      );
    }

    function prediction() {
      const tags = request.params.getAll('tags')
      console.log(tags)
      return ok({
        '2009': {'posts_x': 0.1225744078, 'posts_y': 0.108763207, 'posts': 0.1674608107},
        '2010': {'posts_x': 0.0934197466, 'posts_y': 0.0423308227, 'posts': 0.0575115315},
        '2011': {'posts_x': 0.153566558, 'posts_y': 0.0361163119, 'posts': 0.0606754039},
        '2012': {'posts_x': 0.228142238, 'posts_y': 0.0178589845, 'posts': 0.0700105729},
        '2013': {'posts_x': 0.3027190857, 'posts_y': 0.014689159, 'posts': 0.089297846},
        '2014': {'posts_x': 0.3082495976, 'posts_y': 0.0770990434, 'posts': 0.1011863872},
        '2015': {'posts_x': 0.3506208097, 'posts_y': 0.3412839281, 'posts': 0.1319705512},
        '2016': {'posts_x': 0.3133698108, 'posts_y': 0.616090033, 'posts': 0.1590640688},
        '2017': {'posts_x': 0.2613612964, 'posts_y': 0.6685418303, 'posts': 0.1719779959},
        '2018': {'posts_x': 0.1770700829, 'posts_y': 0.6801485808, 'posts': 0.1598052794},
        '2019': {'posts_x': 0.1269002858, 'posts_y': 0.7168421113, 'posts': 0.1525956232},
        '2020': {'posts_x': 0.1003826625, 'posts_y': 0.6146450567, 'posts': 0.1224838084}
      });
    }

    function comparison() {
      return ok({
        '2020': {'posts_x': 0.1225744078, 'posts_y': 0.108763207, 'posts': 0.1674608107}
      });
    }

    function handleRoute() {
      console.log(url)
      switch (true) {
        case url.includes('google.com') && url.endsWith('/users/authenticate') && method === 'POST':
          return authenticate();
        case url.includes('google.com') && url.endsWith('/users/register') && method === 'POST':
          return register();
        case url.includes('google.com') && url.endsWith('/users') && method === 'GET':
          return getUsers();
        case url.includes('google.com') && url.match(/\/users\/\d+$/) && method === 'GET':
          return getUserById();
        case url.includes('google.com') && url.match(/\/users\/\d+$/) && method === 'PUT':
          return updateUser();
        case url.includes('google.com') && url.match(/\/users\/\d+$/) && method === 'DELETE':
          return deleteUser();
        case url.includes('google.com') && url.endsWith('/tags'):
          return getTags();
        case url.includes('google.com') && url.includes('/current/trend'):
          return currentTrend();
        case url.includes('google.com') && url.includes('/prediction'):
          return prediction();
        case url.includes('google.com') && url.includes('/comparison'):
          return comparison();
        default:
          // pass through any requests not handled above
          return next.handle(request);
      }
    }

    // route functions

    function authenticate() {
      const {username, password} = body;
      const user = users.find(x => x.username === username && x.password === password);
      if (!user) {
        return error('Username or password is incorrect');
      }
      return ok({
        ...basicDetails(user),
        token: 'fake-jwt-token'
      })
    }

    function register() {
      const user = body

      if (users.find(x => x.username === user.username)) {
        return error('Username "' + user.username + '" is already taken')
      }

      user.id = users.length ? Math.max(...users.map(x => x.id)) + 1 : 1;
      users.push(user);
      localStorage.setItem(usersKey, JSON.stringify(users));
      return ok();
    }

    function getUsers() {
      if (!isLoggedIn()) {
        return unauthorized();
      }
      return ok(users.map(x => basicDetails(x)));
    }

    function getUserById() {
      if (!isLoggedIn()) {
        return unauthorized();
      }

      const user = users.find(x => x.id === idFromUrl());
      return ok(basicDetails(user));
    }

    function updateUser() {
      if (!isLoggedIn()) {
        return unauthorized();
      }

      const params = body;
      const user = users.find(x => x.id === idFromUrl());

      // only update password if entered
      if (!params.password) {
        delete params.password;
      }

      // update and save user
      Object.assign(user, params);
      localStorage.setItem(usersKey, JSON.stringify(users));

      return ok();
    }

    function deleteUser() {
      if (!isLoggedIn()) {
        return unauthorized();
      }

      users = users.filter(x => x.id !== idFromUrl());
      localStorage.setItem(usersKey, JSON.stringify(users));
      return ok();
    }

    // helper functions

    function ok(body?) {
      return of(new HttpResponse({status: 200, body}))
        .pipe(delay(500)); // delay observable to simulate server api call
    }

    function error(message) {
      return throwError({error: {message}})
        .pipe(materialize(), delay(500), dematerialize()); // call materialize and dematerialize to ensure delay even if an error is thrown (https://github.com/Reactive-Extensions/RxJS/issues/648);
    }

    function unauthorized() {
      return throwError({status: 401, error: {message: 'Unauthorized'}})
        .pipe(materialize(), delay(500), dematerialize());
    }

    function basicDetails(user) {
      const {id, username, firstName, lastName} = user;
      return {id, username, firstName, lastName};
    }

    function isLoggedIn() {
      return headers.get('Authorization') === 'Bearer fake-jwt-token';
    }

    function idFromUrl() {
      const urlParts = url.split('/');
      return parseInt(urlParts[urlParts.length - 1]);
    }
  }
}

export const fakeBackendProvider = {
  // use fake backend in place of Http service for backend-less development
  provide: HTTP_INTERCEPTORS,
  useClass: FakeBackendInterceptor,
  multi: true
};
