console.log("Meeting page detected");

if (window.location.hostname.includes("meet.google.com")) {
  console.log("Google Meet detected");
}

if (window.location.hostname.includes("teams.microsoft.com")) {
  console.log("Microsoft Teams detected");
}
