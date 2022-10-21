import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, catchError, map, of } from 'rxjs';
import { TokenModel } from './../models/token-model';
import { CookieService } from 'ngx-cookie';




@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _isLoggedIn$ = new BehaviorSubject<boolean>(false);
  isLoggedIn = this._isLoggedIn$.asObservable();


  constructor(private http: HttpClient,private cookieService: CookieService) {
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



  public login(email: string, password: string) {
    const payload = { "email": email, "password": password };
    console.log(JSON.stringify(payload));

    const httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    }    
    return this.http
      .post<TokenModel>('//127.0.0.1:8000/api/login/', JSON.stringify(payload), httpOptions,)
      .pipe(
        map((data) => {
          let token = data as TokenModel;
          console.log(token);
          localStorage.setItem('auth_token', JSON.stringify(token.access));
          this._isLoggedIn$.next(true);

          // var userInfo = this.jwtService.decodeToken(
          //   token.access_token
          // ) as UserProfile;

          // this.userProfile.next(userInfo);

          // return true;
        }),
        catchError((error) => {
          console.log(error);
          return of(false);
        })
      );
  }
}

