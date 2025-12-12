import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Download, Settings, Activity, Zap, Play, Search, X, List, Globe, MoreHorizontal, Save, Folder, Clock } from 'lucide-react';
import AnimatedButton from './components/AnimatedButton';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [url, setUrl] = useState('');
  const [stats, setStats] = useState({ total_downloads: 0, total_size: 0, avg_quality: 0 });

  // Real Config State
  const [config, setConfig] = useState({
    downloadPath: '',
    maxConcurrent: 3,
    quality: '1080p',
    theme: 'dark'
  });

  useEffect(() => {
    fetch('/api/config')
      .then(res => res.json())
      .then(data => {
        // Map backend nested config to frontend flat structure
        setConfig({
          downloadPath: data.download?.output_directory || '',
          maxConcurrent: data.download?.max_concurrent || 3,
          quality: data.download?.default_quality || '1080p',
          theme: 'dark' // Theme not stored in backend yet
        });
      })
      .catch(console.error);
  }, []);

  // Fetch Stats on Mount & Periodically
  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch('/api/stats');
        if (res.ok) {
          const data = await res.json();
          setStats(data);
        }
      } catch (e) {
        console.error("API Error:", e);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleStartDownload = async () => {
    if (!url) return;
    try {
      const res = await fetch('/api/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      const data = await res.json();
      if (data.success) {
        console.log("Download Started:", data.id);
        setActiveTab('downloads');
        setUrl('');
      }
    } catch (e) {
      console.error("Download Failed:", e);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <nav className="sidebar">
        <div className="logo-area">
          <Zap size={28} color="var(--accent-color)" />
          <span className="logo-text">RedLight<span className="logo-suffix">DL</span></span>
        </div>

        <div className="nav-links">
          <NavButton icon={<Activity />} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <NavButton icon={<Globe />} label="Search" active={activeTab === 'search'} onClick={() => setActiveTab('search')} />
          <NavButton icon={<List />} label="Playlist" active={activeTab === 'playlist'} onClick={() => setActiveTab('playlist')} />
          <NavButton icon={<Download />} label="Downloads" active={activeTab === 'downloads'} onClick={() => setActiveTab('downloads')} />
          <NavButton icon={<Clock />} label="History" active={activeTab === 'history'} onClick={() => setActiveTab('history')} />
          <NavButton icon={<MoreHorizontal />} label="Extras" active={activeTab === 'extras'} onClick={() => setActiveTab('extras')} />
          <div className="spacer" style={{ flex: 1 }} />
          <NavButton icon={<Settings />} label="Settings" active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} />
        </div>
      </nav>

      {/* Main Content */}
      <main className="main-content">
        <header className="top-bar">
          <div className="search-bar">
            {/* Changing icon based on context if needed, keeping generic for now */}
            <Search size={18} className="search-icon" />
            <input
              type="text"
              placeholder={activeTab === 'playlist' ? "Paste Playlist URL..." : "Paste URL to download..."}
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
            {url && (
              <motion.button
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="clear-btn"
                onClick={() => setUrl('')}
              >
                <X size={14} />
              </motion.button>
            )}
          </div>
          <AnimatedButton variant="primary" onClick={handleStartDownload}>
            <Play size={18} fill="currentColor" /> {activeTab === 'playlist' ? 'Fetch List' : 'Start'}
          </AnimatedButton>
        </header>

        <div className="content-area">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="tab-content"
              style={{ height: '100%' }}
            >
              {activeTab === 'dashboard' && <DashboardView stats={stats} />}
              {activeTab === 'search' && <SearchView />}
              {activeTab === 'playlist' && <PlaylistView />}
              {activeTab === 'downloads' && <DownloadsView />}
              {activeTab === 'history' && <HistoryView />}
              {activeTab === 'extras' && <ExtrasView />}
              {activeTab === 'settings' && <SettingsView config={config} setConfig={setConfig} />}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

const NavButton = ({ icon, label, active, onClick }) => (
  <motion.div
    className={`nav-btn ${active ? 'active' : ''}`}
    onClick={onClick}
    whileHover={{ x: 5, backgroundColor: 'rgba(255,255,255,0.05)' }}
    whileTap={{ scale: 0.98 }}
  >
    {icon}
    <span>{label}</span>
    {active && (
      <motion.div
        className="active-indicator"
        layoutId="activeTab"
        transition={{ type: "spring", stiffness: 300, damping: 30 }}
      />
    )}
  </motion.div>
);

const DashboardView = ({ stats }) => (
  <div className="view-container">
    <h1 className="hero-title">Ready to <span className="highlight">Accelerate?</span></h1>
    <p className="hero-subtitle">Paste a link above to start downloading securely and anonymously.</p>

    <div className="stats-grid">
      <StatCard label="Total Downloads" value={stats.total_downloads || 0} />
      <StatCard label="Total Size" value={formatBytes(stats.total_size || 0)} />
      <StatCard label="Avg Quality" value={`${stats.avg_quality || 0}p`} />
    </div>
  </div>
);

function formatBytes(bytes, decimals = 2) {
  if (!+bytes) return '0 Bytes';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}

const SearchView = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setSearching(true);
    try {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      const data = await res.json();
      setResults(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error(e);
    } finally {
      setSearching(false);
    }
  };

  return (
    <div className="view-container">
      <h2>Search Engine</h2>
      <p className="text-secondary" style={{ marginBottom: 16 }}>Search across multiple sites simultaneously.</p>

      <div style={{ display: 'flex', gap: 12, marginBottom: 24 }}>
        <input
          type="text"
          placeholder="Search for videos..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          style={{
            flex: 1,
            padding: '12px 16px',
            borderRadius: 8,
            border: '1px solid rgba(255,255,255,0.1)',
            background: 'rgba(255,255,255,0.05)',
            color: '#fff',
            fontSize: 14,
            outline: 'none'
          }}
        />
        <AnimatedButton onClick={handleSearch} disabled={searching} variant="primary">
          {searching ? <Activity size={18} className="spin" /> : <Search size={18} />}
          {searching ? 'Searching...' : 'Search'}
        </AnimatedButton>
      </div>

      <div className="search-results-list">
        {results.map((item, idx) => (
          <div key={idx} style={{
            padding: 16,
            borderBottom: '1px solid rgba(255,255,255,0.08)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <div>
              <h4 style={{ margin: 0, fontSize: 14, fontWeight: 500 }}>{item.title}</h4>
              <p style={{ margin: '4px 0 0', fontSize: 12, color: '#888' }}>
                {item.duration} • {item.site || 'Unknown'}
              </p>
            </div>
            <AnimatedButton onClick={() => {/* Could copy URL or start download */ }}>
              <Download size={14} />
            </AnimatedButton>
          </div>
        ))}
        {!searching && results.length === 0 && (
          <p className="text-secondary" style={{ textAlign: 'center', padding: 40 }}>
            Enter a query to search across all supported sites.
          </p>
        )}
      </div>
    </div>
  );
};

const PlaylistView = () => {
  const [url, setUrl] = useState('');
  const [limit, setLimit] = useState(10);
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const fetchPlaylist = async () => {
    if (!url) return;
    setLoading(true);
    try {
      const res = await fetch(`/api/playlist?url=${encodeURIComponent(url)}&limit=${limit}`);
      const data = await res.json();
      if (data.videos) {
        setVideos(data.videos);
      } else if (data.error) {
        console.error(data.error);
        setVideos([]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const downloadAll = async () => {
    setDownloading(true);
    try {
      const res = await fetch('/api/playlist/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url, limit })
      });
      const data = await res.json();
      if (data.success) {
        alert(`Started ${data.downloads.length} downloads!`);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="view-container">
      <h2>Playlist Downloader</h2>
      <p className="text-secondary" style={{ marginBottom: 16 }}>Batch download videos from channels or playlists.</p>

      <div style={{ display: 'flex', gap: 12, marginBottom: 16, flexWrap: 'wrap' }}>
        <input
          type="text"
          placeholder="Channel or Playlist URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{
            flex: 1,
            minWidth: 200,
            padding: '12px 16px',
            borderRadius: 8,
            border: '1px solid rgba(255,255,255,0.1)',
            background: 'rgba(255,255,255,0.05)',
            color: '#fff',
            fontSize: 14,
            outline: 'none'
          }}
        />
        <input
          type="number"
          placeholder="Limit"
          value={limit}
          onChange={(e) => setLimit(parseInt(e.target.value) || 10)}
          style={{
            width: 80,
            padding: '12px 16px',
            borderRadius: 8,
            border: '1px solid rgba(255,255,255,0.1)',
            background: 'rgba(255,255,255,0.05)',
            color: '#fff',
            fontSize: 14,
            outline: 'none'
          }}
        />
        <AnimatedButton onClick={fetchPlaylist} disabled={loading} variant="primary">
          {loading ? <Activity size={18} className="spin" /> : <List size={18} />}
          {loading ? 'Fetching...' : 'Fetch Videos'}
        </AnimatedButton>
      </div>

      {videos.length > 0 && (
        <div style={{ marginBottom: 16 }}>
          <AnimatedButton onClick={downloadAll} disabled={downloading} variant="primary">
            <Download size={18} />
            {downloading ? 'Starting...' : `Download All (${videos.length})`}
          </AnimatedButton>
        </div>
      )}

      <div className="playlist-videos" style={{ maxHeight: 400, overflowY: 'auto' }}>
        {videos.map((videoUrl, idx) => (
          <div key={idx} style={{
            padding: '10px 12px',
            background: 'rgba(255,255,255,0.03)',
            borderRadius: 6,
            marginBottom: 8,
            fontSize: 13,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}>
            <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }}>
              {idx + 1}. {videoUrl}
            </span>
          </div>
        ))}
        {videos.length === 0 && !loading && (
          <div className="empty-state">
            <List size={48} className="text-secondary" />
            <p>Enter a channel URL and click "Fetch Videos"</p>
          </div>
        )}
      </div>
    </div>
  );
};

const DownloadsView = () => {
  const [downloads, setDownloads] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchDownloads = async () => {
    try {
      const res = await fetch('/api/downloads/active');
      if (res.ok) {
        const data = await res.json();
        setDownloads(Array.isArray(data) ? data : []);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (id) => {
    try {
      await fetch('/api/cancel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ download_id: id })
      });
      fetchDownloads();
    } catch (e) {
      console.error("Cancel failed", e);
    }
  };

  useEffect(() => {
    fetchDownloads();
    const interval = setInterval(fetchDownloads, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="view-container">
      <h2>Active Downloads</h2>
      {loading && downloads.length === 0 ? (
        <div className="loading-state">
          <Activity className="spin" /> Loading...
        </div>
      ) : downloads.length === 0 ? (
        <div className="empty-state">
          <Download size={48} className="text-secondary" />
          <p>No active downloads.</p>
        </div>
      ) : (
        <div className="downloads-list">
          {downloads.map((item) => (
            <div key={item.download_id} className="download-card" style={{
              background: 'rgba(255,255,255,0.05)',
              borderRadius: 12,
              padding: 16,
              marginBottom: 12,
              border: '1px solid rgba(255,255,255,0.1)'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8, alignItems: 'center' }}>
                <h4 style={{ margin: 0, fontSize: 14, fontWeight: 500 }}>{item.title || item.url}</h4>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span className="badge" style={{
                    background: 'var(--accent-color)',
                    color: '#fff',
                    padding: '2px 8px',
                    borderRadius: 4,
                    fontSize: 10
                  }}>{item.status}</span>
                  <AnimatedButton
                    onClick={() => handleCancel(item.download_id)}
                    style={{
                      padding: '2px 8px',
                      fontSize: 12,
                      background: 'rgba(255, 59, 48, 0.2)',
                      color: '#ff3b30',
                      border: '1px solid rgba(255, 59, 48, 0.3)',
                      height: 'auto',
                      minHeight: '20px'
                    }}
                  >
                    <X size={12} style={{ marginRight: 4 }} /> Cancel
                  </AnimatedButton>
                </div>
              </div>

              <div className="progress-bar-container" style={{
                height: 6,
                background: 'rgba(255,255,255,0.1)',
                borderRadius: 3,
                overflow: 'hidden',
                marginBottom: 8
              }}>
                <motion.div
                  className="progress-bar"
                  initial={{ width: 0 }}
                  animate={{ width: `${item.progress_percent}%` }}
                  style={{
                    height: '100%',
                    background: 'var(--accent-color)'
                  }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, color: '#888' }}>
                <span>{item.quality}p • {item.site || 'Unknown'}</span>
                <span>{item.progress_percent ? item.progress_percent.toFixed(1) : 0}%</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );

};
const ExtrasView = () => <div className="placeholder-view"><h2>Extras</h2><p>Converters, Metadata Editors, etc.</p></div>;

const SettingsView = ({ config, setConfig }) => {
  const [loading, setLoading] = useState(false);

  // Initial fetch is handled by parent, but we handle saves here
  const handleChange = (e) => {
    const { name, value } = e.target;
    setConfig(prev => ({ ...prev, [name]: value }));
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config)
      });
      const data = await res.json();
      if (data.success) {
        // Optional: show toast
        console.log("Config saved!", data.config);
      }
    } catch (e) {
      console.error("Save failed", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="view-container settings-view">
      <h2>Configuration</h2>
      <div className="settings-grid">
        <div className="setting-item">
          <label>Download Path</label>
          <div className="input-with-icon">
            <Folder size={18} />
            <input type="text" name="downloadPath" value={config.downloadPath || ''} onChange={handleChange} />
          </div>
        </div>

        <div className="setting-item">
          <label>Max Concurrent Downloads</label>
          <select name="maxConcurrent" value={config.maxConcurrent || 3} onChange={handleChange}>
            <option value="1">1</option>
            <option value="3">3</option>
            <option value="5">5</option>
            <option value="10">Unlimited</option>
          </select>
        </div>

        <div className="setting-item">
          <label>Default Quality</label>
          <select name="quality" value={config.quality || '1080p'} onChange={handleChange}>
            <option value="4k">4K Ultra HD</option>
            <option value="1080p">1080p Full HD</option>
            <option value="720p">720p HD</option>
            <option value="480p">480p SD</option>
          </select>
        </div>

        <div className="setting-item">
          <label>Theme</label>
          <select name="theme" value={config.theme || 'dark'} onChange={handleChange}>
            <option value="dark">Cyberpunk Dark</option>
            <option value="light">Light (Experimental)</option>
          </select>
        </div>
      </div>

      <div className="settings-actions">
        <AnimatedButton variant="primary" onClick={handleSave} disabled={loading}>
          <Save size={18} /> {loading ? 'Saving...' : 'Save Config'}
        </AnimatedButton>
      </div>
    </div>
  );
};

const StatCard = ({ label, value }) => (
  <motion.div
    className="stat-card"
    whileHover={{ y: -5, borderColor: 'var(--accent-color)' }}
  >
    <h3>{value}</h3>
    <p>{label}</p>
  </motion.div>
);

const HistoryView = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetch('/api/downloads/history?limit=50')
      .then(res => res.json())
      .then(data => setHistory(data))
      .catch(console.error);
  }, []);

  return (
    <div className="view-container">
      <h2>Download History</h2>
      <div className="history-list">
        {history.length === 0 ? (
          <p className="empty-state">No downloads yet.</p>
        ) : (
          <table className="history-table" style={{ width: '100%', borderCollapse: 'collapse', marginTop: '20px' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.1)', textAlign: 'left' }}>
                <th style={{ padding: '10px' }}>Date</th>
                <th style={{ padding: '10px' }}>Title</th>
                <th style={{ padding: '10px' }}>Quality</th>
                <th style={{ padding: '10px' }}>Site</th>
              </tr>
            </thead>
            <tbody>
              {Array.isArray(history) && history.map((item) => (
                <tr key={item.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                  <td style={{ padding: '10px', color: '#888' }}>{new Date(item.date_downloaded).toLocaleDateString()}</td>
                  <td style={{ padding: '10px' }}>{item.title || item.filename}</td>
                  <td style={{ padding: '10px', color: 'var(--accent-color)' }}>{item.quality}p</td>
                  <td style={{ padding: '10px', textTransform: 'capitalize' }}>{item.site || 'Unknown'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default App;
