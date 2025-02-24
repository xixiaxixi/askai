import click
from .config import Config
from .core.openai_client import OpenAIClient
from .utils.config_manager import ConfigManager
from . import __version__

@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(__version__, prog_name="askai")
@click.argument('question', nargs=-1, required=False)
@click.option('--prompt', '-p', help='System prompt for the AI')
@click.option('--model', default="deepseek-chat", help='Model to use')
@click.option('--url', help='Base URL for API')
@click.option('--ak', help='API Key')
@click.option('--set-api-key', help='Set default API key in config')
@click.option('--set-base-url', help='Set default base URL in config')
def ask(question, prompt, model, url, ak, set_api_key, set_base_url):
    """
    Ask a question to AI and get the response

You can ask questions with or without quotes:
    askai what is python
    askai "what is python"
    askai how do you say hello in Chinese?

Environment Variables:
    OPENAI_API_KEY: Your API key for authentication
    OPENAI_BASE_URL: Base URL for API endpoint (optional)
    """

    config_manager = ConfigManager()

    # 处理配置设置
    if set_api_key:
        config_manager.set_api_key(set_api_key)
        click.secho(f"API key [${set_api_key[:2]}${'*'*(len(set_api_key)-4)}${set_api_key[-2:]}] has been saved to config", fg='green')
        if not question:
            return

    if set_base_url:
        config_manager.set_base_url(set_base_url)
        click.secho(f"Base URL [${set_base_url}] has been saved to config", fg='green')
        if not question:
            return


    # 将多个参数组合成完整的问题
    full_question = ' '.join(question) if question else None

    # 显示帮助信息的情况
    if not full_question or full_question.lower().strip() == 'help':
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    try:
        # 优先使用命令行参数，其次使用配置文件，最后使用环境变量
        config = Config(
            api_key=ak or config_manager.get_api_key(),
            base_url=url or config_manager.get_base_url(),
            model=model
        )
        client = OpenAIClient(config)
        client.ask(full_question, prompt)

    except Exception as e:
        click.secho(f"Error: {str(e)}", err=True, fg='red')
        exit(0)

if __name__ == '__main__':
    pass