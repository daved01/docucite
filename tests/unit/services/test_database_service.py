from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os
import pytest

from docucite.constants import AppConstants
from docucite.services.database_service import DatabaseService
from docucite.errors import DatabaseError

from tests import BaseTest
from tests.unit.services import DocuciteTestSetup


class TestDatabaseService(BaseTest, DocuciteTestSetup):
    def test_create_database_database_exists(self, mock_logger, mocker):
        with pytest.raises(DatabaseError):
            db_service = DatabaseService(mock_logger, "database_already_exists")

            mocker.patch.object(db_service, "_dir_exists", return_value=True)

            db_service.create_database()

    def test_create_database_base_folder_exists(self, mock_logger, mocker):
        # If
        db_service = DatabaseService(logger=mock_logger, database_name=None)
        mocker.patch.object(db_service, "_dir_exists", side_effect=[False, True])
        makedirs_mock = mocker.patch("os.makedirs", return_value=None)

        # When
        db_service.create_database()

        # Then
        assert db_service.vectordb != None
        assert type(db_service.vectordb.embeddings) == OpenAIEmbeddings
        makedirs_mock.assert_not_called()

    def test_create_database_base_folder_not_exists(self, mock_logger, mocker):
        # If
        db_service = DatabaseService(logger=mock_logger, database_name=None)
        mocker.patch.object(db_service, "_dir_exists", side_effect=[False, False])
        mocker.patch("os.path.exists", return_value=False)
        makedirs_mock = mocker.patch("os.makedirs", return_value=None)

        # When
        db_service.create_database()

        # Then
        assert db_service.vectordb != None
        assert type(db_service.vectordb.embeddings) == OpenAIEmbeddings
        assert (
            makedirs_mock.call_count == 2
        )  # langchain Chroma dependency calls os.makedirs() too
        makedirs_mock.assert_any_call(AppConstants.DATABASE_BASE_DIR)

    def test_update_database(
        self, mock_logger, mock_documents, mock_documents_best_book
    ):
        # Create database in memory with the mock_documents
        db_service = DatabaseService(logger=mock_logger, database_name=None)

        db_service.vectordb = Chroma.from_documents(
            mock_documents_best_book,
            db_service.embedding,
            persist_directory=db_service.database_path,
        )

        ids_first_docs = db_service.vectordb.get().get("ids")

        # When
        db_service.add_documents(mock_documents)

        # Then
        ids_second_docs = db_service.vectordb.get().get("ids")
        assert len(ids_first_docs) == 1
        assert len(ids_second_docs) == 3
        assert ids_first_docs[0] in ids_second_docs

    def test_update_database_not_exist(self, mock_logger, mock_documents):
        with pytest.raises(DatabaseError):
            db_service = DatabaseService(mock_logger, "database_does_not_exist")
            db_service.add_documents(mock_documents)

    def test_create_base_dir(self, mock_logger, tmpdir):
        db_service = DatabaseService(mock_logger, "")
        db_service._create_base_dir()

        assert os.path.exists(AppConstants.DATABASE_BASE_DIR)

    def test_create_base_dir_exist(self, mock_logger, tmpdir, mocker):
        mocker.patch("os.path.exists", return_value=True)
        makedirs_spy = mocker.spy(os, "makedirs")

        db_service = DatabaseService(mock_logger, "")
        db_service._create_base_dir()

        makedirs_spy.assert_not_called()
