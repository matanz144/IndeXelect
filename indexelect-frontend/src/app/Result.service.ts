import {Injectable} from '@angular/core';
import {Subject, Observable} from 'rxjs';

@Injectable()
export class ResultService {
  // results: any = [{indexes: [], min_volume: 0}];
  private submitted = new Subject<any>();
  private projList = new Subject<any>();
  private showResults = new Subject<any>();
  showRes(show: any) {
    return this.showResults.next(show);
  }
  getShowRes(): Observable<any> {
    return this.showResults.asObservable();
  }
  submitResults(results: any) {
    this.submitted.next(results);
  }
  getResults(): Observable<any> {
    return this.submitted.asObservable();
  }
  submitRecords(records: any) {
    this.projList.next(records);
  }
  getRecords(): Observable<any> {
    return this.projList.asObservable();
  }
}
