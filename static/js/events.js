document.addEventListener('DOMContentLoaded', () => {
    const eventsContainer = document.getElementById('eventsContainer');
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');

    let allEvents = [];

    // Fetch events from the API
    async function loadEvents() {
        try {
            const response = await fetch('/events/');
            if (!response.ok) throw new Error('Failed to fetch events');

            const data = await response.json();
            allEvents = data.events || [];

            renderEvents(allEvents);
        } catch (error) {
            console.error('Error loading events:', error);
            eventsContainer.innerHTML = '<div class="no-events"><h3>Failed to load events</h3><p>Please try again later.</p></div>';
        }
    }

    // Render events to the page
    function renderEvents(events) {
        if (events.length === 0) {
            eventsContainer.innerHTML = '<div class="no-events"><h3>No events found</h3><p>Try adjusting your filters or check back later!</p></div>';
            return;
        }

        eventsContainer.innerHTML = events.map(event => `
            <article class="event-card window">
                <div class="title-bar">
                    <button aria-label="Close" disabled class="close hidden"></button>
                    <h3 class="title">${event.title}</h3>
                    <button aria-label="Resize" disabled class="resize hidden"></button>
                </div>
                <div class="separator"></div>
                <div class="window-pane event-body">
                    <p><strong>Category:</strong> <span class="event-category">${event.category || 'Uncategorized'}</span></p>
                    <div class="event-meta">
                        <div class="event-meta-item">
                            <strong>Date:</strong>
                            ${formatDate(event.date)}
                        </div>
                        <div class="event-meta-item">
                            <strong>Location:</strong>
                            ${event.location || 'TBA'}
                        </div>
                    </div>
                    <p class="event-description">${event.description || 'No description provided'}</p>
                    <div class="btn-group">
                        <button class="btn" onclick="viewEvent('${event._id}')">View Details</button>
                        <button class="btn" onclick="openEditModal('${event._id}')">Edit</button>
                    </div>
                </div>
            </article>
        `).join('');
    }

    // Format date for display
    function formatDate(dateString) {
        if (!dateString) return 'TBA';
        const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
        try {
            return new Date(dateString).toLocaleDateString(undefined, options);
        } catch {
            return dateString;
        }
    }

    // Filter events based on search and category
    function filterEvents() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedCategory = categoryFilter.value;

        const filtered = allEvents.filter(event => {
            const matchesSearch = event.title.toLowerCase().includes(searchTerm) ||
                                (event.description && event.description.toLowerCase().includes(searchTerm));
            const matchesCategory = !selectedCategory || event.category === selectedCategory;
            return matchesSearch && matchesCategory;
        });

        renderEvents(filtered);
    }

    // Event listeners for filtering
    searchInput.addEventListener('input', filterEvents);
    categoryFilter.addEventListener('change', filterEvents);

    // Load events on page load
    loadEvents();

    // Expose loadEvents globally for refresh after create/edit/delete
    window.reloadEvents = loadEvents;
});

// Modal Management
function openCreateModal() {
    document.getElementById('createModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeCreateModal() {
    document.getElementById('createModal').classList.remove('active');
    document.body.style.overflow = 'auto';
    document.getElementById('createEventForm').reset();
    updateAIStatus('createAIGenStatus', '');
}

function closeViewModal() {
    document.getElementById('viewModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

function closeEditModal() {
    document.getElementById('editModal').classList.remove('active');
    document.body.style.overflow = 'auto';
    document.getElementById('editEventForm').reset();
    updateAIStatus('editAIGenStatus', '');
}

function updateAIStatus(elementId, message, isError = false) {
    const status = document.getElementById(elementId);
    if (!status) return;

    status.textContent = message;
    status.classList.toggle('error', Boolean(isError));
}

async function requestGeneratedDescription({ title, category, location }) {
    const response = await fetch('/events/generate-description', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, category, location })
    });

    const payload = await response.json();

    if (!response.ok) {
        throw new Error(payload.error || 'Failed to generate description');
    }

    return payload.description;
}

async function generateCreateDescription() {
    const title = document.getElementById('title').value.trim();
    const category = document.getElementById('category').value.trim();
    const location = document.getElementById('location').value.trim();
    const button = document.getElementById('createAIGenBtn');

    if (!title) {
        updateAIStatus('createAIGenStatus', 'Enter a title first.', true);
        return;
    }

    try {
        button.disabled = true;
        updateAIStatus('createAIGenStatus', 'Generating description...');

        const description = await requestGeneratedDescription({ title, category, location });
        document.getElementById('description').value = description;
        updateAIStatus('createAIGenStatus', 'Description generated.');
    } catch (error) {
        console.error('Error generating description:', error);
        updateAIStatus('createAIGenStatus', error.message, true);
    } finally {
        button.disabled = false;
    }
}

async function generateEditDescription() {
    const title = document.getElementById('editTitle').value.trim();
    const category = document.getElementById('editCategory').value.trim();
    const location = document.getElementById('editLocation').value.trim();
    const button = document.getElementById('editAIGenBtn');

    if (!title) {
        updateAIStatus('editAIGenStatus', 'Enter a title first.', true);
        return;
    }

    try {
        button.disabled = true;
        updateAIStatus('editAIGenStatus', 'Generating description...');

        const description = await requestGeneratedDescription({ title, category, location });
        document.getElementById('editDescription').value = description;
        updateAIStatus('editAIGenStatus', 'Description generated.');
    } catch (error) {
        console.error('Error generating description:', error);
        updateAIStatus('editAIGenStatus', error.message, true);
    } finally {
        button.disabled = false;
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const createModal = document.getElementById('createModal');
    const viewModal = document.getElementById('viewModal');
    const editModal = document.getElementById('editModal');

    if (e.target === createModal) closeCreateModal();
    if (e.target === viewModal) closeViewModal();
    if (e.target === editModal) closeEditModal();
});

// Create Event
async function submitCreateEvent(event) {
    event.preventDefault();

    const eventData = {
        title: document.getElementById('title').value,
        category: document.getElementById('category').value,
        date: document.getElementById('date').value,
        location: document.getElementById('location').value,
        description: document.getElementById('description').value
    };

    try {
        const response = await fetch('/events/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(eventData)
        });

        if (!response.ok) throw new Error('Failed to create event');

        closeCreateModal();
        window.reloadEvents();
        alert('Event created successfully!');
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to create event. Please try again.');
    }
}

// View Event
async function viewEvent(eventId) {
    try {
        const response = await fetch(`/events/${eventId}`);
        if (!response.ok) throw new Error('Failed to fetch event');

        const event = await response.json();
        const viewBody = document.getElementById('viewEventBody');

        const dateStr = event.date ? new Date(event.date).toLocaleString() : 'TBA';

        viewBody.innerHTML = `
            <div class="event-details">
                <div class="detail-item">
                    <strong>Category:</strong>
                    <span class="category-badge">${event.category || 'Uncategorized'}</span>
                </div>
                <div class="detail-item">
                    <strong>Date & Time:</strong>
                    <span>${dateStr}</span>
                </div>
                <div class="detail-item">
                    <strong>Location:</strong>
                    <span>${event.location || 'TBA'}</span>
                </div>
                <div class="detail-item">
                    <strong>Description:</strong>
                    <p>${event.description || 'No description provided'}</p>
                </div>
            </div>
            <div class="form-actions">
                <button class="btn" onclick="closeViewModal()">Close</button>
            </div>
        `;

        document.getElementById('viewEventTitle').textContent = event.title;
        document.getElementById('viewModal').classList.add('active');
        document.body.style.overflow = 'hidden';
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load event details.');
    }
}

// Open Edit Modal
async function openEditModal(eventId) {
    try {
        const response = await fetch(`/events/${eventId}`);
        if (!response.ok) throw new Error('Failed to fetch event');

        const event = await response.json();

        document.getElementById('editEventId').value = eventId;
        document.getElementById('editTitle').value = event.title;
        document.getElementById('editCategory').value = event.category || '';
        document.getElementById('editLocation').value = event.location || '';
        document.getElementById('editDescription').value = event.description || '';

        // Format date for datetime-local input
        if (event.date) {
            const date = new Date(event.date);
            const iso = date.toISOString().slice(0, 16);
            document.getElementById('editDate').value = iso;
        }

        document.getElementById('editModal').classList.add('active');
        document.body.style.overflow = 'hidden';
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to load event for editing.');
    }
}

// Submit Edit Event
async function submitEditEvent(event) {
    event.preventDefault();

    const eventId = document.getElementById('editEventId').value;
    const eventData = {
        title: document.getElementById('editTitle').value,
        category: document.getElementById('editCategory').value,
        date: document.getElementById('editDate').value,
        location: document.getElementById('editLocation').value,
        description: document.getElementById('editDescription').value
    };

    try {
        const response = await fetch(`/events/${eventId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(eventData)
        });

        if (!response.ok) throw new Error('Failed to update event');

        closeEditModal();
        window.reloadEvents();
        alert('Event updated successfully!');
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update event. Please try again.');
    }
}

// Delete Event
async function deleteEvent() {
    if (!confirm('Are you sure you want to delete this event?')) return;

    const eventId = document.getElementById('editEventId').value;

    try {
        const response = await fetch(`/events/${eventId}`, {
            method: 'DELETE'
        });

        if (!response.ok) throw new Error('Failed to delete event');

        closeEditModal();
        window.reloadEvents();
        alert('Event deleted successfully!');
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to delete event. Please try again.');
    }
}
