'use strict';

/* global document_base_url, current_user */
/* exported addNotification, update_document_list */

// Add new notifications
function addNotification(notification) {
  // we can show the notification
  if (window.Notification && Notification.permission === 'granted') {
    var data = {
      body: notification.message,
      icon: notification.icon,
      tag: '\'notifications_' + notification.language,
      url: notification.url
    };
    var note = new Notification(notification.title, data);
    // on click the user is directred to the obj detail page
    note.onclick(function (event) {
      event.preventDefault();
      window.document.location = '' + document_base_url + notification.slug + '/';
    });
  }
}

function update_document_detail(data) {
  var read = [];
  var update = [];
  var statusElement = document.getElementById(data.document + '-status');
  if (statusElement) {
    if (data.read) {
      read = Object.entries(data.read).filter(function (user) {
        return user[0] !== current_user;
      });
    }
    if (data.update) {
      update = Object.entries(data.update).filter(function (user) {
        return user[0] !== current_user;
      });
    }
    statusElement.classList.remove('is-success', 'is-warning', 'is-danger');
    if (update.length > 0) {
      statusElement.textContent = 'write';
      statusElement.classList.add('is-danger');
      statusElement.title = update.map(function (item) {
        return item[1];
      }).join(', ');
    } else if (read.length > 0) {
      statusElement.textContent = 'read';
      statusElement.classList.add('is-warning');
      statusElement.title = read.map(function (item) {
        return item[1];
      }).join(', ');
    } else if (statusElement) {
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