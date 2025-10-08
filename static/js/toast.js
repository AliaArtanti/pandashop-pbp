// Toast helper function - Global (no export)
function showToast(message, type) {
  type = type || "info";
  
  var stack = document.getElementById("toast-stack");
  if (!stack) {
    console.error("Toast stack element not found!");
    return;
  }

  var toast = document.createElement("div");
  toast.className = "toast " + type;
  toast.textContent = message;
  
  stack.appendChild(toast);

  setTimeout(function() { 
    toast.style.opacity = "0"; 
  }, 2500);
  
  setTimeout(function() { 
    toast.remove(); 
  }, 3000);
}

// Attach to window object for global access
window.showToast = showToast;