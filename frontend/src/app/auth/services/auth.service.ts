import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, catchError, map, Observable, of, tap } from 'rxjs';
import { TokenModel } from './../models/token-model';
import { CookieService } from 'ngx-cookie';
import { Router } from '@angular/router';
import { RegisterModel } from '../models/register-model';




@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private  myURL = `//127.0.0.1:8000/api/`;
  private _isLoggedIn$ = new BehaviorSubject<boolean>(false);
  isLoggedIn = this._isLoggedIn$.asObservable();


  constructor(private http: HttpClient,private cookieService: CookieService, private router :Router) {
    const token = localStorage.getItem('auth_token');
    this._isLoggedIn$.next(!!token)
  

    
   }


   
 
   getCookie(key: string){
    return this.cookieService.get(key);
  }


  //  public tryfetch()
  //  {
  //   return this.http
  //     .get('//127.0.0.1:8000/api/users/')
  //     .pipe(
  //       map((data) => {
  //        console.log(data);
  //          return true;
  //       }),
  //       catchError((error) => {
  //         console.log(error);
  //         return of(false);
  //       })
  //     );
  // }



  public login(email: string, password: string): Observable<any> {
    const payload = { "email": email, "password": password };
    console.log(JSON.stringify(payload));

    const httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    }    
     return this.http
      .post(`${this.myURL}login/`, JSON.stringify(payload), httpOptions,)
      .pipe(
        tap((data) => {
          let token = data as TokenModel;
          localStorage.setItem('auth_token', JSON.stringify(token.access));
          this._isLoggedIn$.next(true);
          this.router.navigate(['home']);
          // var userInfo = this.jwtService.decodeToken(
          //   token.access_token
          // ) as UserProfile;

          // this.userProfile.next(userInfo);
        })
      );
  }







  public register( username : string, email: string, password: string) {

    const payload = {"username": username ,"email": email, "password": password, "password2": password, "date_of_birth": "2000-01-01T00:00:00Z" };
    console.log(JSON.stringify(payload));

    const httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    }    
    return this.http
      .post<RegisterModel>(`${this.myURL}register/`, JSON.stringify(payload), httpOptions,)
      .pipe(
        tap((data) => {
          this.router.navigate(['login']);
        })
      );
  }



}

