import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from beast.tag import tag
from beast.scripts.tagging import tag_complex
from beast.TreeTagger.treetagger import tag_treetagger

class Compatibility(unittest.TestCase):
    def test_call_defaults_do_not_accumulate_models(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);model=root/'model';model.mkdir();(model/'UD.pt').touch()
            lex=root/'lex';lex.mkdir();(lex/'default').touch();(lex/'default_ud').touch()
            with patch('beast.tag.tag_complex') as call:
                for _ in range(2):tag(src='test',model=str(model),lexicons_path=str(lex),quiet=True)
                self.assertEqual(call.call_count,2)
                self.assertEqual([x.args[13] for x in call.call_args_list],[['UD.pt'],['UD.pt']])
                self.assertEqual(call.call_args_list[0].args[14]['ud'],str(lex/'default_ud'))
    def test_stale_output_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);model=root/'model';model.mkdir();out=root/'out';out.mkdir()
            source=root/'input.txt';source.write_text('test\n',encoding='utf-8')
            stale=out/'input.txt_model.tt';stale.write_text('preserved',encoding='utf-8')
            with self.assertRaises(FileExistsError):tag_complex(str(model),'',[str(source)],str(out),'',models=['UD.pt'])
            self.assertEqual(stale.read_text(encoding='utf-8'),'preserved')
    def test_tree_tagger_path_without_trailing_separator(self):
        with patch('beast.TreeTagger.treetagger.check_call') as run:
            tag_treetagger('model.par','input.txt','output.txt',False,False,tt_path='C:/example/bin')
            self.assertEqual(Path(run.call_args.args[0][0]),Path('C:/example/bin/tree-tagger.exe'))

if __name__=='__main__':unittest.main()
