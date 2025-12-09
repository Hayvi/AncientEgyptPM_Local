
// Mock Server for Ancient Egypt
// Simulates the backend protocol to allow offline play.

(function () {
    console.log("[MockServer] Initializing...");

    // Store original io if it exists, though we likely want to replace it entirely
    var originalIo = window.io;

    // --- Mock Socket Class ---
    class MockSocket {
        constructor() {
            this.callbacks = {};
            this.id = "mock_socket_id_" + Math.random();
            this.connected = true;

            // Simulate connection delay
            setTimeout(() => {
                this.trigger('connect');
                console.log("[MockServer] Socket Connected");
            }, 100);
        }

        on(event, callback) {
            if (!this.callbacks[event]) {
                this.callbacks[event] = [];
            }
            this.callbacks[event].push(callback);
        }

        emit(event, data, callback) {
            console.log("[MockServer] Client emitted:", event, data);

            // Handle specific game events
            if (event === 'message' || event === 'request') { // Adjust based on game's emit 'request' seen in HAR
                this.handleMessage(data, callback);
            } else if (event === 'account') {
                // Verify logic
                if (callback) callback({ status: "ok" });
            }
        }

        trigger(event, ...args) {
            if (this.callbacks[event]) {
                this.callbacks[event].forEach(cb => cb(...args));
            }
        }

        handleMessage(payload, callback) {
            // Basic Pragmatic Play Protocol Mock
            // payload usually object like { type: "...", ... }

            if (!payload || typeof payload !== 'object') return;

            var response = null;

            switch (payload.type) {
                case 'auth':
                case 'login':
                    console.log("[MockServer] Handling Auth");
                    response = {
                        type: "login_response",
                        status: "OK",
                        balance: 10000.00,
                        currency: "USD",
                        nickname: "OfflinePlayer"
                    };
                    break;

                case 'init':
                case 'balance':
                    console.log("[MockServer] Handling Init/Balance");
                    response = {
                        type: "balance_response",
                        balance: 10000.00,
                        status: "OK"
                    };
                    break;

                case 'spin':
                case 'bet':
                    console.log("[MockServer] Handling Spin");
                    // Generate random stops (0-10 roughly)
                    var randomStops = [
                        Math.floor(Math.random() * 10),
                        Math.floor(Math.random() * 10),
                        Math.floor(Math.random() * 10),
                        Math.floor(Math.random() * 10),
                        Math.floor(Math.random() * 10)
                    ];

                    response = {
                        type: "spin_response",
                        stops: randomStops,
                        win: 0, // No win logic for now
                        balance: 9990.00, // Deduct bet
                        status: "OK"
                    };
                    break;

                default:
                    // Generic Acknowledgement to prevent hangs
                    console.log("[MockServer] Unknown message type:", payload.type);
                    if (payload.command) {
                        response = { command: payload.command, status: "ok" };
                    }
                    else {
                        response = { status: "ok" };
                    }
                    break;
            }

            if (response && callback) {
                setTimeout(() => callback(response), 50);
            } else if (response) {
                // If no callback, maybe emit a 'message' event back?
                setTimeout(() => this.trigger('message', response), 50);
            }
        }

        // Stub other methods
        disconnect() { }
        close() { }
    }

    // --- Override Global io ---
    window.io = function (url, options) {
        console.log("[MockServer] io() called with:", url);
        return new MockSocket();
    };

    // Also patch window.WebSocket just in case, though they likely use io
    // window.WebSocket = ... 

    console.log("[MockServer] Ready. Global 'io' function overridden.");

})();
