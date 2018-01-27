/*global channels, users_count_path, document_path, current_user, notifications_path, addNotification, update_document_detail, update_document_list */
'use strict';

window.addEventListener('load', function () {
  Notification.requestPermission(function (status) {
    if (Notification.permission !== status) {
      Notification.permission = status;
    }
  });
});

if (notifications_path) {
  // Library is instantiated and connected to the endpoint
  var notifications = new channels.WebSocketBridge();
  notifications.connect(notifications_path);
  // Demultiplexing frontend-side
  notifications.demultiplex('document', function (action, stream) {
    var title = void 0;
    // action is used to provide a title to the notification
    if (action.action === 'update') {
      title = 'Document updated';
    } else if (action.action === 'create') {
      title = 'Document created';
    } else if (action.action === 'delete') {
      title = 'Document deleted';
    }
    // helper function to construct the notification from the object serialization
    addNotification(title, action.data);
  });
  notifications.listen(function (data) {});
}

if (users_count_path) {
  // Library is instantiated and connected to the endpoint
  var users_count = new channels.WebSocketBridge();
  users_count.connect(users_count_path);
  // whenever a message is received, the user counter is updated
  users_count.listen(function (data) {
    if (data.users) {
      document.getElementById('users-counter').textContent = data.users;
    }
  });
}

if (document_path) {
  // Library is instantiated and connected to the endpoint
  var document_status = new channels.WebSocketBridge();
  document_status.connect(document_path);
  // whenever a message is received, the documents badges is updated
  document_status.listen(function (data) {
    if (data.document) {
      // we only have one document - detail view
      update_document_detail(data);
    } else {
      // all documents - list view
      update_document_list(data);
    }
  });
}