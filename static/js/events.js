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
            <div class="event-card">
                <div class="event-header">
                    <span class="event-category">${event.category || 'Uncategorized'}</span>
                    <h3>${event.title}</h3>
                </div>
                <div class="event-body">
                    <div class="event-meta">
                        <div class="event-meta-item">
                            <strong>📅 Date:</strong>
                            ${formatDate(event.date)}
                        </div>
                        <div class="event-meta-item">
                            <strong>📍 Location:</strong>
                            ${event.location || 'TBA'}
                        </div>
                    </div>
                    <p class="event-description">${event.description || 'No description provided'}</p>
                </div>
                <div class="event-footer">
                    <div class="btn-group">
                        <button class="btn btn-view" onclick="viewEvent('${event._id}')">View Details</button>
                        <button class="btn btn-edit" onclick="editEvent('${event._id}')">Edit</button>
                    </div>
                </div>
            </div>
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
});

// Placeholder functions for future implementation
function viewEvent(eventId) {
    alert(`View event: ${eventId}`);
    // TODO: Implement event detail view
}

function editEvent(eventId) {
    alert(`Edit event: ${eventId}`);
    // TODO: Implement event edit modal
}
