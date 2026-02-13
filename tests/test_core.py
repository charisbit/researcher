"""
Unit tests for research-agent
"""

import pytest
import os
from unittest.mock import patch, MagicMock


class TestConfig:
    """Test Config class"""

    def test_default_config(self, tmp_path):
        """Test default configuration loading"""
        with patch("research_agent.config.os.path.exists", return_value=False):
            from research_agent.config import Config

            config = Config(tmp_path / "nonexistent.yaml")

            assert config.get_model("test_agent") == "anthropic.claude-3-sonnet-latest"
            assert config.is_using_local() is False

    def test_get_model_cloud(self, tmp_path):
        """Test getting cloud model"""
        config_content = """
defaults:
  cloud_model: anthropic.claude-3-haiku-latest
  local_model: llama3.2:latest
  use_local: false

agents:
  web_searcher:
    cloud: claude-3-opus
    local: llama3.2:latest
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        from research_agent.config import Config

        with patch.dict(os.environ, {}, clear=True):
            config = Config(str(config_file))

            # Test default cloud model
            assert (
                config.get_model("unknown_agent") == "anthropic.claude-3-haiku-latest"
            )

            # Test agent-specific cloud model
            assert config.get_model("web_searcher") == "claude-3-opus"

    def test_get_model_local(self, tmp_path):
        """Test getting local model"""
        config_content = """
defaults:
  cloud_model: claude-3-sonnet
  local_model: llama3.2:latest
  use_local: true
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        from research_agent.config import Config

        with patch.dict(os.environ, {}, clear=True):
            config = Config(str(config_file))

            # Should use local model when use_local is true
            assert config.is_using_local() is True

    def test_environment_override(self, tmp_path):
        """Test environment variable override"""
        config_content = """
defaults:
  cloud_model: claude-3-sonnet
  local_model: llama3.2:latest
  use_local: false
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        from research_agent.config import Config

        with patch.dict(os.environ, {"USE_LOCAL_MODEL": "true"}):
            config = Config(str(config_file))
            assert config.is_using_local() is True

    def test_get_ollama_config(self, tmp_path):
        """Test getting Ollama configuration"""
        config_content = """
ollama:
  base_url: http://ollama:11434
  api_key: secret
  timeout: 120
"""
        config_file = tmp_path / "config.yaml"
        config_file.write_text(config_content)

        from research_agent.config import Config

        config = Config(str(config_file))
        ollama_config = config.get_ollama_config()

        assert ollama_config["base_url"] == "http://ollama:11434"
        assert ollama_config["timeout"] == 120


class TestModelSwitcher:
    """Test ModelSwitcher class"""

    def test_check_ollama_status_not_running(self):
        """Test checking Ollama status when not running"""
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)

            from research_agent.model_switcher import ModelSwitcher

            ms = ModelSwitcher()
            import asyncio

            result = asyncio.run(ms.check_ollama_status())
            assert result is False

    def test_list_models_structure(self):
        """Test model listing returns correct structure"""
        import asyncio
        from research_agent.model_switcher import ModelSwitcher

        ms = ModelSwitcher()

        # Mock the check_ollama_status to return False (no local models)
        async def mock_check():
            return False

        with patch.object(ms, "check_ollama_status", mock_check):
            result = asyncio.run(ms.list_available_models())

            assert "cloud" in result
            assert "local" in result
            assert isinstance(result["cloud"], list)
            assert isinstance(result["local"], list)


class TestResearchAgent:
    """Test research agent components"""

    def test_agent_import(self):
        """Test that agent modules can be imported"""
        from research_agent import config, model_switcher

        assert hasattr(config, "Config")
        assert hasattr(model_switcher, "model_switcher")

    def test_config_singleton(self):
        """Test that config is a singleton"""
        from research_agent.config import config, Config

        assert isinstance(config, Config)


class TestPackageMetadata:
    """Test package metadata"""

    def test_package_info(self):
        """Test package can be imported"""
        import research_agent

        assert research_agent.__name__ == "research_agent"

    def test_version_info(self):
        """Test version information exists"""
        from importlib.metadata import version

        try:
            v = version("research-agent")
            assert v is not None
        except Exception:
            pytest.skip("Package not installed")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
