window.onpageshow = function(event) {
    if (window.performance.navigation.type==2) {
        window.location.reload();
    }
    if (event.persisted) {
        window.location.reload(false);
   }
};