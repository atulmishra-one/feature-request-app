/**
*@author atul mishra
**/

function ClientValue(data){
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
}

function AreaValue(data){
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
}

function featureAppModel(){
    var self = this;

    self.title = ko.observable("");
    self.description = ko.observable("");
    self.clientValues = ko.observableArray([]);
    self.selectedClient = ko.observable(1);
    self.priority = ko.observable(1);
    self.target_date = ko.observable(moment().format("YYYY-MM-DD"));
    self.areaValues = ko.observableArray([]);
    self.selectedArea = ko.observable(new AreaValue({"name": "Reports", "id": "Reports"}));

    $.getJSON('/api/client_values', function(values){
        var results = $.map(values, function(value){
            return new ClientValue(value);
        });
        self.clientValues(results);
    });

    $.getJSON('/api/areas_values', function(values){
        var results = $.map(values, function(value){
            return new AreaValue(value);
        });
        self.areaValues(results);
    });

    $.getJSON('/api/list_features', function(results){
          console.log(results.length);
          var table = '';
          if( results.length > 0 ){
            for(i=0; i < results.length; i++){
                table += "<tr><td>"+results[i].title+"</td>\
                <td>"+results[i].description+"</td><td>"+results[i].client+"</td><td>"+results[i].priority+"</td>\
                <td>"+results[i].target_date+"</td><td>"+results[i].product_area+"</td><td>\
                <button class='btn btn-danger delete' id="+results[i].id+">Remove</button></td></tr>";
            }
          }else{
             table = '<tr><td colspan="6" align="middle">\
             No feature has been submitted. Click the add button to add a new feature.</td></tr>';
          }
          $('#feature_content').append(table);
    });

    $(document).on('click', '.btn.btn-danger.delete', function(event){
        self.deleteFeature(event.currentTarget.id, this);
    });

    self.create = function(formElement){
        // Validate the form
        $(formElement).validate();
        if( !$(formElement).valid() ){
            return false;
        }
        form_array = $(formElement).serializeArray();
        request_data = {};
        $.each($(formElement).serializeArray(), function(i, row){
            request_data[row.name] = row.value;
        });

        $.ajax({
            url: '/api/request_new_feature',
            data: JSON.stringify(request_data),
            type: 'POST',
            contentType: "application/json; charset=utf-8",
        }).done(function(response){
            alert(response.message);
        }).fail(function(xhr){
            alert(xhr.message);
        });
    };

    self.deleteFeature = function(id, row){
        if( ! confirm("Are you sure, you want to delete this feature.")){
            return false;
        }

        $.ajax({
            url: '/api/delete_feature',
            data: JSON.stringify({"id": id}),
            type: 'DELETE',
            contentType: "application/json; charset=utf-8",
        }).done(function(response){
            row.closest('tr').remove();
        }).fail(function(xhr){
            alert(xhr.message);
        });
    };

}

ko.applyBindings(new featureAppModel(), document.querySelector('[role=main]'));
