

document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Call sendMail function on submission of form
  document.querySelector('form').onsubmit = function() {

    //call send mail function
    sendMail();

    //prevents the default submission of the form which involves either 
    //reloading the current page or redirecting to a new one
    return false;
  };
});

function sendMail() {
  //get values submitted with form
  const sendTo = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const content = document.querySelector('#compose-body').value;

  //call API to send emails
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: sendTo,
        subject: subject,
        body: content
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);

      //if result throws an error, reload compose page with error
      if ('error' in result) {
        sendToError = result;
        compose_email(sendToError);
      }

      //if successful redirect to sent mailbox
      else {
        load_mailbox('sent');
      }
  })
  .catch(error => {
    console.log('Error: ', error);
  });
}

//write new email
function compose_email(sendToError) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emailContent-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  //if required, take error and display on page
  if ('error' in sendToError) {
    document.querySelector('#sendToError').innerHTML = sendToError['error'];
  }
}

//load mailbox view
function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emailContent-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  // document.querySelector('#emails-view').append(<h2>Test</h2>);

  //prepare string for use with API
  prefix = '/emails/';
  mailboxRequest = prefix.concat(mailbox);

  //request emails from server via API
  fetch(mailboxRequest)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // ... do something else with emails ...\
      //create array for for loops to refer to when displaying emails
      const displayColumns = ["sender", "subject", "timestamp"];

      //select what is currently being displayed on the webpage
      const currentView = document.querySelector('#emails-view');

      //create new container for rows and columns
      const newContainer = document.createElement('div');
      newContainer.classname = "container";
      newContainer.id = "emailContainer";

      //create new rows
      for (i = 0; i < emails.length; i++) {
        const newRow = document.createElement('div');
        newRow.className = "row border my-1";
        newRow.id = emails[i]["id"];

        //create new columns, and small elements for rows
        for (x = 0; x < displayColumns.length; x++) {
          const newColumn = document.createElement('div');
          const newSmall = document.createElement('small');
          
          //initalise background colours if email is read or not (white for unread, grey for read)
          if (emails[i]["read"] == true) {
            newColumn.className = 'col bg-light';
          }
          
          else {
            newColumn.className = 'col';
          }

          //add in text properties per column
          if (x == 0) {
            newSmall.className = 'font-weight-bold text-left'
          }

          if (x == 1) {
            newSmall.className = 'font-weight-normal'
          }

          if (x == 2) {
            newSmall.className = 'font-weight-light'
          }

          //add small content to column, add content to row
          newSmall.innerHTML = emails[i][displayColumns[x]];
          newColumn.appendChild(newSmall);
          newRow.appendChild(newColumn);
        }

        //attach event listener to new row
        newRow.addEventListener('click', function() {
          emailContent(newRow.id);
        });

        //add new row to container
        newContainer.appendChild(newRow);
      }

      //add new container to current view
      currentView.appendChild(newContainer);
  });
}

//view email content view
function emailContent(emailID) {
  fetch('/emails/' + emailID)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
  
      // ... do something else with email ...
      //hide other views, display email content view
      document.querySelector('#emails-view').style.display = 'none';
      document.querySelector('#compose-view').style.display = 'none';
      document.querySelector('#emailContent-view').style.display = 'block';

      //select email content view and make it blank
      const emailView = document.querySelector('#emailContent-view');
      emailView.innerHTML = '';

      //create new header
      const headerContainer = document.createElement('div');
      headerContainer.className = 'container';

      //get email info to display in header, replace for converting various characters to increase readability
      let emailSender = "<b>From: </b> " + email["sender"] + "<br />";
      let emailRecipients = "<b>To: </b>" + email["recipients"] + "<br />";
      let emailSubject = "<b>Subject: </b>" + email["subject"] + "<br />";
      let emailTimestamp = "<b>Timestamp: </b>" + email["timestamp"] + "<br />";
      let emailBody = email["body"].replace(/\n/g, '<br/>');

      //display email info in header
      const emailInfo = document.createElement('p');
      emailInfo.innerHTML = emailSender + emailRecipients + emailSubject + emailTimestamp;

      //append emailInfo to header container
      headerContainer.appendChild(emailInfo);

      //appender header container to view
      emailView.appendChild(headerContainer);

      //reply button
      const replyButton = document.createElement('button');
      replyButton.innerHTML = 'Reply';
      replyButton.className = 'btn btn-primary btn-sm';
      headerContainer.appendChild(replyButton);

      //attach event listener to reply button
      replyButton.addEventListener('click', function() {
        replyEmail(email["sender"], email["subject"], email["timestamp"], email["body"]);
      })

      //get useremail from top of HTML file
      const getUserEmail = JSON.parse(document.querySelector('#getUserEmail').textContent);

      //remove archive button if in user's sent box
      if (getUserEmail != email["sender"]) {

        //display archive or unarchive button
        const archiveButton = document.createElement('button');
        archiveButton.className = 'btn btn-secondary btn-sm mx-2';
        if (email["archived"] == false) {
          archiveButton.innerHTML = 'Archive';
          booleanStatus = true;
        }

        else {
          archiveButton.innerHTML = 'Unarchive';
          booleanStatus = false;
        }

        //attach event listener to new row
        archiveButton.addEventListener('click', function() {
          archiveEmail(email["id"], booleanStatus);
          load_mailbox('inbox');
        });

        //add button to header container
        headerContainer.appendChild(archiveButton);
      }      

      //new container to display email body
      const emailBodyDisplay = document.createElement('div');
      emailBodyDisplay.className = 'container';

      //add horizontal line break
      emailBodyDisplay.innerHTML += '<hr>';

      //add email body below horizontal break
      emailBodyDisplay.innerHTML += '<p>' + emailBody + '</p>';

      //add header and body containers to view
      emailView.appendChild(headerContainer);
      emailView.appendChild(emailBodyDisplay);

      //mark email as read
      fetch('/emails/' + emailID, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      });
  });
}

//reply to email
function replyEmail(sender, subject, timestamp, body) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#emailContent-view').style.display = 'none';

  // prefill composition fields composition fields
  document.querySelector('#compose-recipients').value = sender;

  if (subject.includes("Re: ")) {
    document.querySelector('#compose-subject').value = subject;
  }

  else {
    document.querySelector('#compose-subject').value = 'Re: ' + subject;
  }

  document.querySelector('#compose-body').value = '\n\nOn ' + timestamp + ' ' + sender + ' wrote: \n\n' + body;
}

//archive email when button archive button is clicked
function archiveEmail(emailID, booleanStatus) {
  fetch('/emails/' + emailID, {
    method: 'PUT',
    body: JSON.stringify({
        archived: booleanStatus
    })
  });
}
