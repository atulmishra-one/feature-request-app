/**
* @author atul mishra
**/

function ClientValue(data){
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
}

function ProductValue(data){
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
    self.products = ko.observableArray([]);
    self.selectedArea = ko.observable(new ProductValue({"name": "Reports", "id": "Reports"}));
    self.features = ko.observableArray([]).extend({ paged: { pageSize: 6 } });

    $.getJSON('/api/clients', function(values){
        var results = $.map(values, function(value){
            return new ClientValue(value);
        });
        self.clientValues(results);
    });

    $.getJSON('/api/products', function(values){
        var results = $.map(values, function(value){
            return new ProductValue(value);
        });
        self.products(results);
    });

    $.getJSON('/api/list_features', function(results){
        self.features(results);
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


    deleteFeature = function(id, event, data){
        if( ! confirm("Are you sure, you want to delete this feature.")){
            return false;
        }

        $.ajax({
            url: '/api/delete_feature',
            data: JSON.stringify({"id": id}),
            type: 'DELETE',
            contentType: "application/json; charset=utf-8",
        }).done(function(response){
            self.features.remove(function(feature){
                return feature.id == id
            });
        }).fail(function(xhr){
            alert(xhr.message);
        });
    };

    self.sortByTitle = function() {
        self.features.sort(function(a, b) {
            return a.title < b.title ? -1 : 1;
        });
    };

    self.sortByPriority = function() {
        self.features.sort(function(a, b) {
            return a.priority < b.priority ? -1 : 1;
        });
    };

    // Pagination
    self.setPage = function(newPage) {
        self.chars.pageNumber(newPage);
    };

}

ko.applyBindings(new featureAppModel(), document.querySelector('[role=main]'));
