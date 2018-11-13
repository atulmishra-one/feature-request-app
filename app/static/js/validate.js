// Wait for the DOM to be ready
$(function() {
  // Initialize form validation on the create feature form.
  $("form[name='create_feature']").validate({
    // Specify validation rules
    rules: {
      title: "required",
      description: "required",
      priority: "required",
      target: {
        required: true,
        date: true
      }
    },
    // Specify validation error messages
    messages: {
      firstname: "Please enter a title.",
      lastname: "Please enter the description.",
      priority: "Please enter a priority number.",
      target: {
        required: "Please enter a target date.",
        date: "Please enter a valid date"
      }
    }
  });
});