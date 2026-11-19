"""
Test data for automation tests
"""

CHECKOUT_DATA = {
    "valid_billing": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "telephone": "1234567890",
        "address_1": "123 Test Street",
        "city": "Test City",
        "postcode": "12345",
        "country": "United States",
        "region": "California"
    },
    "invalid_billing": {
        "first_name": "",
        "last_name": "",
        "email": "invalid-email",
        "telephone": "",
        "address_1": "",
        "city": "",
        "postcode": "",
        "country": "",
        "region": ""
    },
    "billing_info": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@test.com",
        "telephone": "1234567890",
        "address_1": "123 Test Street",
        "city": "Test City",
        "postcode": "12345",
        "country": "United States",
        "region": "California"
    },
    "guest_info": {
        "first_name": "Guest",
        "last_name": "User",
        "email": "guest@test.com",
        "telephone": "9876543210"
    }
}

CONTACT_DATA = {
    "valid_contact": {
        "name": "Test User",
        "email": "testuser@example.com",
        "subject": "Test Inquiry",
        "message": "This is a test message for automation testing purposes."
    },
    "valid_enquiry": {
        "name": "Test User",
        "email": "testuser@example.com",
        "enquiry": "This is a test enquiry for automation testing purposes."
    },
    "invalid_contact": {
        "name": "",
        "email": "invalid-email",
        "subject": "",
        "message": ""
    },
    "invalid_email": {
        "name": "Test User",
        "email": "not-an-email",
        "enquiry": "Test message with invalid email"
    },
    "long_message": {
        "name": "Test User",
        "email": "test@example.com",
        "enquiry": "This is an extremely long message that exceeds the typical character limit for contact form messages. " * 50 + "This message is designed to test the form's handling of very long text inputs and should trigger validation or truncation mechanisms if they exist in the system."
    },
    "empty_form": {
        "name": "",
        "email": "",
        "message": ""
    }
}

USER_DATA = {
    "test_user": {
        "email": "testuser@example.com",
        "password": "Test123!",
        "first_name": "Test",
        "last_name": "User"
    },
    "new_user": {
        "first_name": "New",
        "last_name": "User",
        "email": "newuser@test.com",
        "password": "NewUser123!",
        "telephone": "1234567890"
    }
}

WISHLIST_DATA = {
    "test_user": {
        "first_name": "Wishlist",
        "last_name": "Tester",
        "email": "wishlist@test.com",
        "password": "Wishlist123!",
        "telephone": "1234567890"
    }
}