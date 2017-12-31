function FeatureRequestModel(data) {
    this.id = ko.observable(data.id);
    this.user = ko.observable(data.user);
    this.client = ko.observable(data.client);
    this.title = ko.observable(data.title);
    this.description = ko.observable(data.description);
    this.client_priority = ko.observable(data.client_priority);
    this.target_date = ko.observable(data.target_date);
    this.created_on = ko.observable(data.created_on);
    this.updated_on = ko.observable(data.updated_on);
    this.product_area = ko.observable(data.product_area);

    this.user_id = ko.observable(data.user_id);
    this.client_id = ko.observable(data.client_id);
    this.product_area_id = ko.observable(data.product_area_id);
}

function ProductAreaModel(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
}

function UserModel(data) {
    this.id = ko.observable(data.id);
    this.first_name = ko.observable(data.first_name);
}

function ClientModel(data) {
    this.id = ko.observable(data.id);
    this.name = ko.observable(data.name);
}

function get_feature_requests(){
    $.getJSON("/api/feature_requests/", function(data) {
        return $.map(data['feature_requests'], function(item) { return new FeatureRequestModel(item) });
    });
}

function FeatureRequestViewModel() {
    var self = this;
    self.featureRequests = ko.observableArray([]);
    self.feature_request = ko.observableArray();

    $.getJSON("/api/feature_requests/", function(data) {
        var mappedFeatures = $.map(data['feature_requests'], function(item) { return new FeatureRequestModel(item) });
        self.featureRequests(mappedFeatures);
    });

    self.users = ko.observableArray([]);
    $.getJSON("/api/users/", function(data) {
        var mappedUsers = $.map(data['users'], function(item) { return new UserModel(item) });
        self.users(mappedUsers);
    });

    self.product_areas = ko.observableArray([]);
    $.getJSON("/api/product_areas/", function(data) {
        var mappedProductAreas = $.map(data['product_areas'], function(item) { return new ProductAreaModel(item) });
        self.product_areas(mappedProductAreas);
    });

    self.clients = ko.observableArray([]);
    $.getJSON("/api/clients/", function(data) {
        var mappedClients = $.map(data['clients'], function(item) { return new ClientModel(item) });
        self.clients(mappedClients);
    });

    self.addRequest = function(form_element) {
        var data = $('#add_fr_form').serializeArray().map(function(x){this[x.name] = x.value; return this;}.bind({}))[0];
        var has_errors = false;
        self.errors = null;

        $.ajax(
            '/api/feature_requests/add/',
            {
                contentType: 'application/json;',
                method: 'POST',
                data: JSON.stringify(data),
                success: function (data) {
                    $('#add_fr').modal('hide');
                    self.featureRequests.push(new FeatureRequestModel(ko.toJS(data['data'][0])));
                    alert(data['message']);
                },
                error: function (errors) {
                    has_errors = true;
                    self.errors = errors.responseJSON.errors;
                }
            });

        if (has_errors){
            self.errors = errors.responseJSON.errors
        }
        else{

        }
    };

    self.setRequest = function(feature_request) {
        self.feature_request(new FeatureRequestModel(ko.toJS(feature_request)));
        $('#edit_fr').modal('show');
    }

    self.updateRequest = function(form_element){
        var data = $('#edit_fr_form').serializeArray().map(function(x){this[x.name] = x.value; return this;}.bind({}))[0];
        var has_errors = false;
        var errors = null;

        $.ajax(
            '/api/feature_requests/' + data.id + '/',
            {
                contentType: 'application/json;',
                method: 'POST',
                data: JSON.stringify(data),
                success: function (new_data) {
                    $('#edit_fr').modal('hide');
                    var oldLocation = ko.utils.arrayFirst(self.featureRequests(), function (item) {
                        return item.id() == data.id;
                    });
                    self.featureRequests.replace(oldLocation, new FeatureRequestModel(ko.toJS(new_data['data'][0])));
                    alert(new_data['message']);
                },
                error: function (errors) {
                    has_errors = true;
                    errors = errors.responseJSON.errors;
                }
            });

        if (has_errors){
            self.errors = errors.responseJSON.errors
        }
    };
}

ko.applyBindings(new FeatureRequestViewModel());