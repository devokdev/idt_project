# Comprehensive Data Structures, Algorithms & Computer Networks Master Guide

## 1. Asymptotic Complexity Analysis & Recurrence Relations

Algorithmic complexity establishes the mathematical bounds on execution time and memory footprint as input size $n \to \infty$:

```
+--------------------+------------------------+-------------------------------------------------------------+
| Notation           | Formal Definition      | Intuitive Meaning                                           |
+--------------------+------------------------+-------------------------------------------------------------+
| Big-O (O)          | T(n) <= c * f(n)       | Asymptotic Upper Bound (Worst-case guarantee)               |
| Big-Omega (Ω)      | T(n) >= c * f(n)       | Asymptotic Lower Bound (Best-case theoretical limit)        |
| Big-Theta (Θ)      | c1*f(n) <= T(n) <= c2  | Asymptotically Tight Bound (Exact growth rate)              |
| Little-o (o)       | lim(n->inf) T(n)/f(n)=0| Strictly looser upper bound (T grows strictly slower)       |
+--------------------+------------------------+-------------------------------------------------------------+
```

### 1.1 The Master Theorem for Divide-and-Conquer Recurrences
Given a recurrence relation of the form:

$$T(n) = aT\left(\frac{n}{b}\right) + f(n)$$

Where $a \ge 1$ (number of subproblems), $b > 1$ (division factor), and $f(n) = \Theta(n^c)$:
1. **Case 1 (Leaf-Heavy)**: If $c < \log_b a$, then $T(n) = \Theta(n^{\log_b a})$.
   - Example: Strassen's Matrix Multiplication $T(n) = 7T(n/2) + \mathcal{O}(n^2) \implies \log_2 7 \approx 2.807 > 2 \implies T(n) = \Theta(n^{2.807})$.
2. **Case 2 (Balanced Work across Levels)**: If $c = \log_b a$, then $T(n) = \Theta(n^c \log n)$.
   - Example: Merge Sort $T(n) = 2T(n/2) + \Theta(n) \implies \log_2 2 = 1 = c \implies T(n) = \Theta(n \log n)$.
3. **Case 3 (Root-Heavy)**: If $c > \log_b a$, and regularity condition holds ($af(n/b) \le kf(n)$ for $k < 1$), then $T(n) = \Theta(f(n))$.
   - Example: $T(n) = 3T(n/4) + n^2 \implies \log_4 3 \approx 0.793 < 2 \implies T(n) = \Theta(n^2)$.

---

## 2. Advanced Non-Linear Data Structures: Trees & Graphs

### 2.1 Self-Balancing Binary Search Trees: AVL vs Red-Black Trees

```
+--------------------------+------------------------------------+------------------------------------+
| Feature                  | AVL Tree                           | Red-Black (RB) Tree                |
+--------------------------+------------------------------------+------------------------------------+
| Balance Invariant        | Height diff between subtrees <= 1  | 1. Every node is Red or Black      |
|                          | (|h_L - h_R| <= 1)                 | 2. Root is Black; Leaves are Black |
|                          |                                    | 3. No two adjacent Red nodes       |
|                          |                                    | 4. Equal Black-height on all paths |
| Strictness of Balance    | Strictly Balanced: h <= 1.44 log N | Loosely Balanced: h <= 2 log(N+1)  |
| Lookup Latency           | Faster (due to smaller tree depth) | Slightly slower                    |
| Insertion / Deletion Cost| Costlier (Up to O(log N) rotations)| Faster (At most 2-3 rotations)     |
| Real-World Use Cases     | Read-heavy lookup dictionaries     | Standard libraries (C++ std::map,  |
|                          |                                    | Java TreeMap, Linux CFS Scheduler) |
+--------------------------+------------------------------------+------------------------------------+
```

### 2.2 Segment Trees with Lazy Propagation
Used for range queries and range updates in $\mathcal{O}(\log N)$ time (e.g., Range Minimum Query, Range Sum):

```python
class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self.build(arr, 0, 0, self.n - 1)

    def build(self, arr, node, l, r):
        if l == r:
            self.tree[node] = arr[l]
            return
        mid = (l + r) // 2
        self.build(arr, 2 * node + 1, l, mid)
        self.build(arr, 2 * node + 2, mid + 1, r)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update_range(self, node, l, r, ql, qr, val):
        if self.lazy[node] != 0:
            self.tree[node] += (r - l + 1) * self.lazy[node]
            if l != r:
                self.lazy[2 * node + 1] += self.lazy[node]
                self.lazy[2 * node + 2] += self.lazy[node]
            self.lazy[node] = 0

        if l > qr or r < ql:
            return
        if ql <= l and r <= qr:
            self.tree[node] += (r - l + 1) * val
            if l != r:
                self.lazy[2 * node + 1] += val
                self.lazy[2 * node + 2] += val
            return

        mid = (l + r) // 2
        self.update_range(2 * node + 1, l, mid, ql, qr, val)
        self.update_range(2 * node + 2, mid + 1, r, ql, qr, val)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
```

### 2.3 Prefix Trie for Autocomplete & Inverted Indexing
A digital search tree where node edges represent individual characters, achieving $\mathcal{O}(L)$ search complexity where $L$ is key length, completely independent of total dictionary size $N$.

---

## 3. Core Algorithmic Paradigms in Technical Interviews

1. **Sliding Window Pattern**:
   - Reduces nested loops from $\mathcal{O}(N^2)$ to $\mathcal{O}(N)$ when evaluating contiguous subarrays/substrings (e.g., Longest Substring Without Repeating Characters, Maximum Sum Subarray of size $K$).
2. **Monotonic Stack / Queue**:
   - Maintains elements in strictly increasing or decreasing order.
   - Solves the Next Greater Element, Largest Rectangle in Histogram, and Daily Temperatures problems in $\mathcal{O}(N)$ linear time.
3. **Topological Sort (Kahn's Algorithm - BFS)**:
   - Evaluates dependency resolution, build systems, and course schedules in Directed Acyclic Graphs (DAGs) in $\mathcal{O}(V + E)$ time using in-degree arrays.

---

## 4. Computer Networks: Transport Protocols & Congestion Control

```
+---------------------+-------------------------------+-------------------------------+-------------------------------+
| Protocol            | TCP (Transmission Control)    | UDP (User Datagram Protocol)  | QUIC / HTTP/3                 |
+---------------------+-------------------------------+-------------------------------+-------------------------------+
| Connection Setup    | 3-Way Handshake (1 RTT)       | Connectionless (0 RTT)        | 1-RTT (Initial) / 0-RTT TLS   |
| Reliability         | Guaranteed (ACK + Retransmit) | Unreliable (Best-effort)      | Guaranteed (Packet multiplex) |
| Ordering            | Strict Byte-Stream in order   | Unordered datagrams           | Multiplexed independent stream|
| Head-of-Line (HoL)  | Suffers HoL at TCP socket     | No HoL blocking               | Zero HoL Blocking at transport|
| Congestion Control  | Built-in (AIMD, BBR, Cubic)   | None (Application managed)    | Built-in congestion control   |
+---------------------+-------------------------------+-------------------------------+-------------------------------+
```

### 4.1 TCP 3-Way Handshake & 4-Way Connection Termination
- **Connection Establishment (3-Way)**:
  1. Client $\to$ Server: `SYN` (Sequence number $x$). Client enters `SYN-SENT`.
  2. Server $\to$ Client: `SYN-ACK` (Sequence number $y$, Acknowledgment $x+1$). Server enters `SYN-RCVD`.
  3. Client $\to$ Server: `ACK` (Acknowledgment $y+1$). Both enter `ESTABLISHED`.
- **Connection Teardown (4-Way)**:
  1. Client $\to$ Server: `FIN` (Client enters `FIN-WAIT-1`).
  2. Server $\to$ Client: `ACK` (Server enters `CLOSE-WAIT`, Client enters `FIN-WAIT-2`).
  3. Server $\to$ Client: `FIN` (Server enters `LAST-ACK`).
  4. Client $\to$ Server: `ACK` (Client enters `TIME-WAIT` for $2 \times \text{MSL} \approx 60\text{ seconds}$ to ensure final ACK was received and drain delayed network packets).

### 4.2 TCP Congestion Control Mechanics (AIMD)
Prevents network collapse by dynamically adjusting the Congestion Window (`cwnd`):
1. **Slow Start**:
   - `cwnd` begins at 10 MSS (Maximum Segment Size).
   - For every ACK received, `cwnd` doubles each RTT (exponential growth: $1 \to 2 \to 4 \to 8 \to \dots$) until it hits `ssthresh` (Slow Start Threshold).
2. **Congestion Avoidance**:
   - When `cwnd >= ssthresh`, exponential growth shifts to linear additive increase: $\text{cwnd} = \text{cwnd} + 1\text{ MSS per RTT}$.
3. **Fast Retransmit & Fast Recovery**:
   - Receipt of **3 Duplicate ACKs** signals an isolated packet loss without waiting for retransmission timer expiration.
   - Retransmits missing segment immediately, halves `ssthresh = cwnd / 2`, sets `cwnd = ssthresh + 3`, avoiding full drop to 1 MSS.
4. **Timeout Event**:
   - If a retransmission timer expires (severe congestion), `ssthresh` is set to $\text{cwnd} / 2$, and `cwnd` is reset to 1 MSS, restarting Slow Start.

### 4.3 Why QUIC (HTTP/3) Solves Head-of-Line Blocking
In HTTP/2, multiple HTTP requests are multiplexed over a single underlying TCP connection. If a single packet is dropped in transit, the OS kernel TCP stack suspends delivery of **all** multiplexed streams until the missing packet is retransmitted. QUIC runs over UDP and implements independent connection encryption and stream framing: packet loss on Stream A has zero impact on Stream B, achieving true zero-head-of-line blocking.
