/*global document_base_url, media_base_url */
'use strict';

// Add new notifications
function addNotification(title, obj) {
  // we can show the notification
  if (window.Notification && Notification.permission === 'granted') {
    const data = {
      body: obj.title,
      icon: `${media_base_url}${obj.image}`,
      url: `${obj.slug}/`,
      tag: obj.slug
    };
    const note = new Notification(title, data);
    // on click the user is directred to the obj detail page
    note.onclick = function (event) {
      event.preventDefault();
      window.document.location = `${document_base_url}${obj.slug}/`;
    };
  }
}

function update_document_detail(data) {
  let read = [], update = [];
  const statusElement = document.getElementById(`${data.document}-status`);
  if (statusElement) {
    if (data.read) {
      read = Object.entries(data.read).filter(user => user[0] !== current_user);
    }
    if (data.update) {
      update = Object.entries(data.update).filter(user => user[0] !== current_user);
    }
    statusElement.classList.remove('is-success', 'is-warning', 'is-danger');
    if (update.length > 0) {
      statusElement.textContent = 'write';
      statusElement.classList.add('is-danger');
      statusElement.title = update.map(item => item[1]).join(', ');
    }
    else if (read.length > 0) {
      statusElement.textContent = 'read';
      statusElement.classList.add('is-warning');
      statusElement.title = read.map(item => item[1]).join(', ');
    }
    else if (statusElement) {
      statusElement.textContent = 'free';
      statusElement.classList.add('is-success');
    }
  }
}


function update_document_list(data) {
  Object.values(data).forEach(function (item) {
    update_document_detail(item);
  });
}
