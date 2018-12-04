// Wait for the DOM to be ready

$(function() {

   $.validator.addMethod("validatePastDate", function(value, element){
        var selectedDate = new Date(value);
        var currentDate = new Date();
        if ( selectedDate < currentDate ){
            return false;
        }
        return true;
   });

  // Initialize form validation on the create feature form.
  $("form[name='create_feature']").validate({
    // Specify validation rules
    rules: {
      title: "required",
      description: "required",
      priority: "required",
      target_date: {
        required: true,
        date: true,
        validatePastDate: true
      }
    },
    // Specify validation error messages
    messages: {
      firstname: "Please enter a title.",
      lastname: "Please enter the description.",
      priority: "Please enter a priority number.",
      target_date: {
        required: "Please enter a target date.",
        date: "Please enter a valid date.",
        validatePastDate: "Target date must be a future date."
      }
    }
  });

});