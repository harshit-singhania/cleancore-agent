import { useState } from 'react'
import ReactDiffViewer from 'react-diff-viewer'
import axios from 'axios'
import './App.css'

const API_URL = 'http://localhost:8000'

function App() {
  const [inputCode, setInputCode] = useState('')
  const [translatedCode, setTranslatedCode] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleTranslate = async () => {
    if (!inputCode.trim()) {
      setError('Please enter ABAP code to translate')
      return
    }

    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.post(`${API_URL}/api/v1/translate-abap`, {
        code: inputCode,
      })

      setTranslatedCode(response.data.translated_code)
    } catch (err) {
      console.error('Translation error:', err)
      setError(
        err.response?.data?.error?.message || 
        'Failed to translate code. Please try again.'
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleClear = () => {
    setInputCode('')
    setTranslatedCode('')
    setError(null)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🚀 CleanCore Agent</h1>
        <p>SAP ABAP to S/4HANA Clean Core Translation</p>
      </header>

      <main className="app-main">
        <div className="toolbar">
          <button 
            className="btn btn-primary"
            onClick={handleTranslate}
            disabled={isLoading}
          >
            {isLoading ? 'Translating...' : 'Translate'}
          </button>
          <button 
            className="btn btn-secondary"
            onClick={handleClear}
            disabled={isLoading}
          >
            Clear
          </button>
        </div>

        {error && (
          <div className="error-banner">
            {error}
          </div>
        )}

        <div className="panes-container">
          <div className="pane input-pane">
            <div className="pane-header">
              <h3>Legacy ABAP Input</h3>
              <span className="pane-badge">Input</span>
            </div>
            <textarea
              className="code-input"
              value={inputCode}
              onChange={(e) => setInputCode(e.target.value)}
              placeholder="Paste your legacy ABAP code here...&#10;&#10;Example:&#10;REPORT ZTEST.&#10;DATA: lv_value TYPE string.&#10;SELECT * FROM ztable INTO TABLE @DATA(lt_data)."
              spellCheck={false}
            />
          </div>

          <div className="pane output-pane">
            <div className="pane-header">
              <h3>S/4HANA Clean Core Output</h3>
              <span className="pane-badge pane-badge-success">Output</span>
            </div>
            {translatedCode ? (
              <div className="diff-container">
                <ReactDiffViewer
                  oldValue={inputCode}
                  newValue={translatedCode}
                  splitView={false}
                  showDiffOnly={false}
                  styles={{
                    variables: {
                      light: {
                        diffViewerBackground: '#f8f9fa',
                        gutterBackground: '#e9ecef',
                        addedBackground: '#d4edda',
                        addedColor: '#155724',
                        removedBackground: '#f8d7da',
                        removedColor: '#721c24',
                      },
                    },
                  }}
                />
              </div>
            ) : (
              <div className="empty-state">
                <p>Translated code will appear here</p>
                <p className="empty-state-hint">
                  Enter legacy ABAP code on the left and click Translate
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="app-footer">
        <p>CleanCore Agent © 2026 | Powered by Gemini 1.5 Flash</p>
      </footer>
    </div>
  )
}

export default App
