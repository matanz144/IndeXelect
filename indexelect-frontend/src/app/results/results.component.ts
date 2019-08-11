import {Component, Input, OnDestroy, OnInit} from '@angular/core';
import {ResultService} from '../Result.service';
import exportFromJSON from 'export-from-json';
import {HttpClient} from '@angular/common/http';
import { Papa } from 'ngx-papaparse';
import {Subscription} from 'rxjs';


@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.css']
})
export class ResultsComponent implements OnInit, OnDestroy {
  constructor(private httpClient: HttpClient,
              public resultService: ResultService,
              private papa: Papa) {
  }

  result = [{indexes: [], min_volume: 0}];
  error = false;
  subscription: Subscription;
  records = [];
  file: any;
  page = 1;
  show = false;


  ngOnInit() {
    this.resultService.getResults().subscribe((results) => {
      this.result = results;
      this.page = 1;
    });
    this.resultService.getRecords().subscribe((records) => {
      this.records = records;
    });
    this.resultService.getShowRes().subscribe( (show) => {
      this.show = show;
      this.addProjectToResults();
    })
  }

  next_result(page) {
    if (page < this.result.length) {
      this.page += 1;
    }
  }

  previous_result(page) {
    if (page > 1) {
      this.page -= 1;
    }
  }

  getSamplesList(records) {
    const samples_list = [];
    for (const item of records) {
      samples_list.push(item.samples);
    }
    return samples_list;
  }

  getProjectList(records) {
    const project_list = [];
    for (let item of records) {
      project_list.push(item.project);
    }
    return project_list;
  }

  sortRecords(dict) {
    let new_dict = [];
    let newlst: any[] = [];
    for (let i of dict) {
      newlst.push(i.samples);
    }
    newlst.sort((n1: any, n2) =>  {
      if (n1 > n2) { return 1; }
      if (n1 < n2) { return - 1; }
      return 0;
    }).reverse();
    for (let v of newlst) { // passing through every value in the samples sorted list
      for (let i of dict) { // check for every item of the dict wich key will set to each value
        if (v === i.samples) {
          new_dict.push({'project': i.project, 'samples': v});
        }
      }
    }
    return new_dict;
  }
  chooseProject (records, num_samples) {
    let new_records = [];
    console.log(num_samples);
    if(num_samples === undefined) {
      return null;
    }
    for (const s of num_samples) {
      for (const r of records) {
        if (s === r.samples) {
          new_records.push(r.project);
        }
      }
    }
    return new_records;
  }
  addProjectToResults() {   // Add project column to results
    const sorted_dict = this.sortRecords(this.records);
    for (const set of this.result) {
      let samples = set['num_samples'];
      let s = 0;
      let count = 0;
      let r = 0;
      let new_records = this.chooseProject(this.records, samples);
      if(samples === undefined) {
        samples = 0;
      }
        // console.log('records are: ' + new_records);
        for (const index of set.indexes) {
          if (count === samples[s]){
            s++;
            r++;
            count = 0;
          }
          index['project'] = new_records[r];
          count ++;
          // console.log('index->project: ' + index.project);
        }
        // console.log('records after shift: ' + new_records);
    }
  }
  downloadFile(filename, data) {
    let blob = new Blob([data], { type: 'text/csv;charset=utf-8' });
    let blobObject = URL.createObjectURL(blob);
    if (navigator.appVersion.toString().indexOf('.NET') > 0)
      window.navigator.msSaveBlob(blob, filename);
    else {
      let link = document.createElementNS('http://www.w3.org/1999/xhtml', 'a');
      link['href'] = blobObject;
      link['download'] = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }

  export_result() {
    let file_data: any;
    let file_name = 'ExportFile_Set_' + this.page + '.csv';
    let set = [];
    for (let i of this.result[this.page - 1].indexes) {
      let index = { Well: String, Id: String, Index_Tag: String, Sequence: String, Volume: Number, Project: String};
      index.Well = i.well;
      index.Id = i.id;
      index.Index_Tag = i.tag;
      index.Sequence = i.sequence;
      index.Volume = i.volume;
      index.Project = i.project;
      set.push(index);
    }
    file_data = this.papa.unparse(set,{ header: true});
    this.downloadFile(file_name, file_data);
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
}
