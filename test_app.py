from app import main

def test_main_output(capsys):
    main()
    captured = capsys.readouterr()
    assert "hey" in captured.out
