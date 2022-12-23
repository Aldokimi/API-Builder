import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, catchError, map, Observable, of, tap } from 'rxjs';
import { TokenModel } from './../models/token-model';
import { CookieService } from 'ngx-cookie';
import { ActivatedRoute, Router } from '@angular/router';
import { RegisterModel } from '../models/register-model';
import { User } from 'src/app/profiles/models/user';




@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private  myURL = `//127.0.0.1:8000/api/`;
  private _isLoggedIn$ = new BehaviorSubject<boolean>(false);
  private _currentUser$ = new BehaviorSubject<any>({});
  private readonly TOKEN_NAME = 'auth_token';
  isLoggedIn = this._isLoggedIn$.asObservable();
  currentUser = this._currentUser$.asObservable();

  get token(){
    return this.getCookie(this.TOKEN_NAME)
  }
  constructor(private http: HttpClient,private cookieService: CookieService, private router :Router,private route: ActivatedRoute) {
    this._isLoggedIn$.next(this.checkSession())
    
  }

   
 
   getCookie(key: string):any|undefined{
    return this.cookieService.get(key);
  }
   putCookie(key:string, value:string)
   {
    this.cookieService.put(key,value);
   }

   deleteCookie(key:string)
   {
    this.cookieService.remove(key);
     }


     /**
 * Returns a hash code from a string
 * @param  {String} str The string to hash.
 * @return {Number}    A 32bit integer
 * @see http://werxltd.com/wp/2010/05/13/javascript-implementation-of-javas-string-hashcode-method/
 */
private  hashCode(str:string) :number {
  let hash = 0;
  for (let i = 0, len = str.length; i < len; i++) {
      let chr = str.charCodeAt(i);
      hash = (hash << 5) - hash + chr;
      hash |= 0; // Convert to 32bit integer
  }
  return hash;
}
 

  public login(email: string, password: string): Observable<any> {
    const payload = { "email": email, "password": password };
    const httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    }    
     return this.http
      .post(`${this.myURL}login/`, JSON.stringify(payload), httpOptions,)
      .pipe(
        tap((data) => {
          let token = data as TokenModel;
          this.putCookie('userid', JSON.stringify(token.id));
          this.putCookie('userid_h', JSON.stringify(this.hashCode(token.id.toString())));
          this.putCookie(this.TOKEN_NAME, JSON.stringify(token.access));
          this._isLoggedIn$.next(this.checkSession());
          this._currentUser$.next(data);
         
          this.router.navigate(['home'], {skipLocationChange: true});
        })
        );
        }


  
        public getCurrentUser(): Observable<User> {

          let header = new HttpHeaders().set(
            'Authorization',
            `Bearer ${this.getCookie('auth_token')}`
          );
           
            return this.http.get<User>(`${this.myURL}users/${this.getCookie('userid')}`);
            
        
        }
      

  public checkSession()
  {
    if (this.getCookie(this.TOKEN_NAME) === undefined || this.getCookie('userid') === undefined || this.getCookie('userid_h') === undefined || this.hashCode(this.getCookie('userid')) !== parseInt(this.getCookie('userid_h')) )
    {
      return false;
    }
    return true;
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

  

  public logout():void{
    this.deleteCookie(this.TOKEN_NAME);
    this.deleteCookie('userid');
    this.deleteCookie('userid_h');
  }


}

