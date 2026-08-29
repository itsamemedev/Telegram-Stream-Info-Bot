# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (195)

```
 10431  GET              /                                                dashboard
 14951  GET              /api/abo/status                                  api_abo_status
 10504  GET              /api/active-recordings                           api_active_recordings
 15022  GET              /api/activity-pulse                              api_activity_pulse
 14829  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 21701  GET/POST         /api/audio/config                                api_audio_config
 21731  POST             /api/audio/testtone                              api_audio_testtone
 14895  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14919  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14923  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11956  GET              /api/automation/status                           api_automation_status
 11978  POST             /api/automation/toggle                           api_automation_toggle
 13756  GET              /api/azrael/agents                               api_azrael_agents
 11848  POST             /api/azrael/ask                                  api_azrael_ask
 21937  GET/POST         /api/azrael/context                              api_azrael_context
 13431  GET              /api/azrael/core                                 api_azrael_core
 22071  POST             /api/azrael/live_pause                           api_azrael_live_pause
 22061  GET              /api/azrael/live_status                          api_azrael_live_status
 22079  POST             /api/azrael/live_test                            api_azrael_live_test
 13765  GET              /api/azrael/memories                             api_azrael_memories
 22127  POST             /api/azrael/persona                              api_azrael_persona_set
 22118  GET              /api/azrael/personas                             api_azrael_personas
 22155  GET              /api/azrael/piper_status                         api_azrael_piper_status
 21910  POST             /api/azrael/react                                api_azrael_react
 21946  GET              /api/azrael/reaction                             api_azrael_reaction
 22098  GET              /api/azrael/reactions                            api_azrael_reactions
 22148  GET              /api/azrael/transcript                           api_azrael_transcript
 22033  POST             /api/azrael/tts_test                             api_azrael_tts_test
 22008  GET              /api/azrael/voices                               api_azrael_voices
 22172  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10803  GET              /api/backoff-watch                               api_backoff_watch
 14306  POST             /api/backup/run                                  api_backup_run
 14272  GET              /api/backup/status                               api_backup_status
 14261  POST             /api/backup/system                               api_backup_system
 14861  GET              /api/bandwidth/live                              api_bandwidth_live
 14814  GET              /api/bookmarks                                   api_bookmarks_list
 11066  GET              /api/brain                                       api_brain
 11003  GET              /api/brain/alarms                                api_brain_alarms
 10988  GET              /api/brain/creator                               api_brain_creator
 10965  GET              /api/brain/graph                                 api_brain_graph
 11026  GET              /api/brain/growth                                api_brain_growth
  9981  GET              /api/brain/health                                api_brain_health
 22653  GET              /api/channel/categories                          api_channel_categories
 22659  POST             /api/channel/set                                 api_channel_set
 22469  GET              /api/channels/status                             api_channels_status
 21345  POST             /api/chat/send                                   api_chat_send
 13960  GET              /api/chat/send_status                            api_chat_send_status
 10485  GET              /api/checks                                      api_checks
 21974  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21957  GET              /api/clips                                       api_clips
 21990  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21623  GET              /api/cohost                                      api_cohost
 21635  POST             /api/cohost/config                               api_cohost_config
 15330  GET              /api/community/stats                             api_community_stats
 23524  GET              /api/data/export                                 api_data_export
 21549  GET              /api/debug/threads                               api_debug_threads
 24351  GET              /api/defense/attacks                             api_defense_attacks
 24318  GET              /api/defense/crowdsec                            api_defense_crowdsec
 24336  GET              /api/defense/fail2ban                            api_defense_fail2ban
 24042  GET              /api/defense/overview                            api_defense_overview
 14368  POST             /api/discord/announce                            api_discord_announce
 14096  GET              /api/discord/clips_week                          api_discord_clips_week
 14312  GET              /api/discord/community                           api_discord_community
 13988  GET              /api/discord/invite                              api_discord_invite
 13562  GET              /api/discord/overview                            api_discord_overview
 13648  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14843  GET              /api/events                                      api_events
 14143  GET              /api/events/stream                               api_events_stream
 14856  GET              /api/forecast/storage                            api_forecast_storage
 11994  GET              /api/freeai/status                               api_freeai_status
 13504  GET              /api/health                                      api_health
 14874  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14870  GET              /api/heatmap/recordings                          api_heatmap_recordings
 21672  GET              /api/highlights                                  api_highlights
 21684  POST             /api/highlights/config                           api_highlights_config
 22510  GET              /api/kick/channel                                api_kick_channel
 22531  POST             /api/kick/channel                                api_kick_channel_set
 13231  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13299  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13277  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13216  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13256  GET              /api/kick/oauth/status                           api_kick_oauth_status
 21749  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 21818  POST             /api/kickmod/config                              api_kickmod_config
 21863  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 21877  GET              /api/kickmod/learned                             api_kickmod_learned
 21904  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 21884  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 22215  POST             /api/kickmod/say                                 api_kickmod_say
 22191  POST             /api/kickmod/start                               api_kickmod_start
 21789  GET              /api/kickmod/status                              api_kickmod_status
 22202  POST             /api/kickmod/stop                                api_kickmod_stop
 10365  POST             /api/login                                       dashboard_login_submit
 15315  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12357  POST             /api/marketing/config                            api_marketing_config
 12382  GET              /api/marketing/preview                           api_marketing_preview
 12392  POST             /api/marketing/send-now                          api_marketing_send_now
 12331  GET              /api/marketing/status                            api_marketing_status
 12349  POST             /api/marketing/toggle                            api_marketing_toggle
 12995  POST             /api/news/config                                 api_news_config
 12961  GET              /api/news/creators                               api_news_creators
 12972  POST             /api/news/creators/generate                      api_news_creators_generate
 13037  POST             /api/news/generate-now                           api_news_generate_now
 13032  GET              /api/news/items                                  api_news_items
 13023  GET              /api/news/preview                                api_news_preview
 12942  GET              /api/news/status                                 api_news_status
 12987  POST             /api/news/toggle                                 api_news_toggle
 15284  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13925  GET              /api/notify/status                               api_notify_status
 13936  POST             /api/notify/test                                 api_notify_test
 10589  GET              /api/outcomes                                    api_outcomes
 23130  POST             /api/overlay/config                              api_overlay_config
 23117  POST             /api/overlay/event                               api_overlay_event
 23022  GET              /api/overlay/state                               api_overlay_state
 10622  GET              /api/profile/<username>                          api_profile
 15040  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14882  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 15005  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14982  GET              /api/proxy/trend                                 api_proxy_trend
 12916  GET              /api/public/stats                                api_public_stats
 10465  GET              /api/pulse                                       api_pulse
 14446  GET              /api/recording-attempts                          api_recording_attempts
 21280  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 21258  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 21299  POST             /api/restream/<int:rid>/start                    api_restream_start
 21570  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 22984  GET              /api/restream/chatfeed                           api_restream_chatfeed
 21234  POST             /api/restream/create                             api_restream_create
 13307  GET              /api/restream/deck                               api_restream_deck
 11930  GET              /api/restream/health                             api_restream_health
 23006  POST             /api/restream/layout                             api_restream_layout
 21207  GET              /api/restream/list                               api_restream_list
 11899  POST             /api/restream/report                             api_restream_report
 21583  POST             /api/restream/start_all                          api_restream_start_all
 21609  POST             /api/restream/stop_all                           api_restream_stop_all
 12105  GET              /api/restream/testpush                           api_testpush_status
 12130  POST             /api/restream/testpush                           api_testpush_run
 15415  GET              /api/restream/verify                             api_restream_verify
 14074  GET              /api/retention/preview                           api_retention_preview
 14083  POST             /api/retention/run                               api_retention_run
 14799  GET              /api/search                                      api_search
 24089  GET              /api/selftest                                    api_selftest
 21316  GET              /api/shield/stats                                api_shield_stats
 10526  GET              /api/storage                                     api_storage
 10533  POST             /api/storage/cleanup                             api_storage_cleanup
 14936  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11869  GET              /api/stream/timeline                             api_stream_timeline
 13636  GET              /api/stream/transcript                           api_stream_transcript
 23272  GET              /api/streamer/compare                            api_streamer_compare
 23471  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14035  GET              /api/streamer/detail                             api_streamer_detail
 23496  GET              /api/streamer/digest/<username>                  api_streamer_digest
 23376  GET              /api/streamer/dormant                            api_streamer_dormant
 23452  GET              /api/streamer/exists/<username>                  api_streamer_exists
 23331  GET              /api/streamer/journal/<username>                 api_streamer_journal
 23296  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 23356  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13471  GET              /api/streamers/wall                              api_streamers_wall
 10557  GET              /api/summary/preview                             api_summary_preview
 14511  GET              /api/system                                      api_system
 15363  GET              /api/system/check_timing                         api_check_timing
 15686  GET              /api/system/config_drift                         api_config_drift
 13672  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13783  GET              /api/system/preflight                            api_system_preflight
 13909  GET              /api/system/preflight_history                    api_system_preflight_history
 14208  GET              /api/system/resilience                           api_system_resilience
 14834  GET              /api/tags                                        api_tags_list
 10499  GET              /api/top                                         api_top
 10858  GET              /api/trend-7d                                    api_trend_7d
 22022  GET              /api/tts/<fn>                                    api_tts_file
 15658  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 15610  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 15634  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 15588  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 23158  GET              /api/upload_window                               api_upload_window
 10603  GET              /api/userstats                                   api_userstats
 13048  GET              /api/version                                     api_version
 15509  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 15530  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 15542  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 15467  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 15491  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 15445  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 27774  GET              /api/youtube/sendrate                            api_youtube_sendrate
 14484  GET              /archive/<int:eid>/download                      archive_download
 14541  GET              /download/<int:recording_id>                     download
 14424  GET              /health                                          health
 21518  GET              /healthz                                         healthz
 10356  GET              /login                                           dashboard_login_page
 10386  GET              /logout                                          dashboard_logout
 10393  GET              /manifest.webmanifest                            pwa_manifest
 13700  GET              /metrics                                         api_prometheus_metrics
 22967  GET              /overlay                                         overlay_page
 10417  GET              /pwa-icon-<variant>.png                          pwa_icon
 10403  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (160)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
```

## Discord-Slash-Commands (45)

```
 24794  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 25253  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 24885  /assign_role            Rolle/Gruppe einem Mitglied geben
 24931  /ban                    Mitglied bannen
 25585  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 25509  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 25549  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 25534  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 25376  /clips                  Letzte Highlight-Clips eines Users
 24846  /create_category        Kategorie anlegen
 24815  /create_channel         Text-Channel anlegen (optional in Kategorie)
 24874  /create_group           Nutzergruppe (= Rolle) anlegen
 24857  /create_role            Rolle / Nutzergruppe anlegen
 24831  /create_voice           Voice-Channel anlegen
 25167  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 25283  /event                  Community-Event ankündigen (Admin) — mit Countdown
 25326  /events                 Kommende Community-Events anzeigen
 25422  /follow                 Bei Live-Gang eines Streamers gepingt werden
 25406  /help                   Alle Bot-Befehle anzeigen
 24920  /kick                   Mitglied kicken
 25149  /leaderboard            Top-10 der Community nach XP
 25362  /livenow                Welche getrackten User sind gerade live
 25392  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 25223  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 24955  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 25135  /rank                   Dein Level und Rang anzeigen
 25349  /recstatus              Aktuell laufende Aufnahmen
 24896  /remove_role            Rolle/Gruppe entfernen
 24808  /restream_status        Restream-Status
 24907  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 25100  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 25118  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 25448  /stats                  Statistik zu einem getrackten Streamer
 24720  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 25744  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 25641  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 25617  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 24942  /timeout                Mitglied stummschalten (Minuten)
 25520  /topstreamers           Rangliste der Streamer nach Aufnahmen
 24750  /track                  TikTok-User tracken
 24734  /tracklist              Getrackte TikTok-User dieses Servers
 25437  /unfollow               Live-Pings für einen Streamer abbestellen
 24783  /untrack                TikTok-User nicht mehr tracken
 25470  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 25494  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 26228  on_member_join
 26190  on_message
 25831  on_raw_reaction_add
 26263  on_ready
```

## Top-Level-Symbole in bot.py (548 Funktionen, 2 Klassen)

```
  2478-2479   _abo_key
  2499-2517   _abo_probe_dump
 23631-23641  _active_recorder_sync
 18504-18511  _ad_allowlist
 19626-19632  _agent_for
 23643-23661  _ai_calls_total_sync
 19635-19651  _ai_telemetry
 20133-20151  _alert
 26376-26426  _alert_monitor_loop
 26805-26867  _announce_loop
  3420-3423   _anthropic_key
  3430-3432   _anthropic_model
 10109-10112  _arg_int
  2470-2475   _as_dict
 16364-16369  _audio_cfg
 20287-20309  _audio_tap_cmd
 10277-10288  _auth_cookie
 10244-10273  _auth_guard
  1626-1631   _auto_on
 21183-21201  _auto_restream_loop
 27935-27950  _azrael_broadcast_reply
 27835-27857  _azrael_chat_reply
 27818-27832  _azrael_chat_should_reply
 12613-12631  _azrael_creator_take
 27863-27865  _azrael_gate_cfg
 19656-19670  _azrael_live_state
 22870-22884  _azrael_overlay_state
 20016-20070  _azrael_proactive_loop
 19475-19531  _azrael_reaction_to_chats
 27868-27875  _azrael_reply_all_chats
 27805-27815  _azrael_self_names
 27903-27932  _azrael_send_to
 19673-19694  _azrael_system
 26545-26548  _backup_active
 26626-26639  _backup_loop
 18392-18393  _badwords_path
 26341-26350  _brain_growth_loop
 10934-10961  _brain_growth_snapshot
  2406-2426   _brain_hint_delay
 10926-10928  _brain_history_for
  6509-6537   _brain_notify
 10903-10924  _brain_record
 10930-10932  _brain_stream_recent
 14122-14139  _browser_push
  6553-6640   _build_daily_summary
  2909-3089   _build_native_cmd
 16712-16899  _build_restream_cmd
  3133-3166   _build_ytdlp_cmd
 23583-23590  _cached_probe
  5331-5358   _can_stop_tracking
  1806-1828   _capture_set_cookies
 15099-15102  _cfg_get
 15105-15107  _cfg_set
 22614-22649  _channel_set_all
 15962-15965  _chat_connected
 15968-15984  _chat_disconnected
  8589-8600   _chat_is_forum
 16004-16006  _chat_sanitize
 16008-16017  _chat_src_ok
 15947-15959  _chat_stat
 15987-15990  _chat_stats_snapshot
  3695-3706   _check_ai_alive_sync
  3709-3721   _check_ai_models_sync
 23592-23605  _check_redis_alive_sync
 23607-23627  _check_redis_version_sync
 14000-14013  _ci_key
 11533-11576  _classify_pool_anonymity
 11579-11596  _classify_pool_anonymity_bg
   783-787    _claude_chat_sync_metered
 10138-10145  _client_ip
 26899-26926  _clip_prune
 26929-26939  _clip_recfile_for
 27455-27461  _clip_should_velocity
 26980-27062  _clip_to_discord
  3593-3602   _close_ai_session
 27979-27994  _cohost_broadcast
 27961-27965  _cohost_cfg
 28020-28032  _cohost_fire_highlight
 27968-27976  _cohost_gate
 27997-28017  _cohost_highlight
 27111-27145  _community_events_loop
 10757-10759  _conv_messages
  6939-6979   _cookie_alarm_loop
  1878-1882   _cookie_autorefresh_info
  1783-1787   _cookie_header
 14172-14204  _cpu_load_snapshot
  3903-3915   _create_index_safe
 12581-12596  _creator_activity
 12637-12660  _creator_dossier_generate
 12599-12610  _creator_facts_line
 23844-23950  _crowdsec_status
 23810-23841  _crowdsec_via_lapi
 23675-23693  _cscli_bin
 23699-23712  _cscli_path
  6832-6857   _daily_summary_loop
 23730-23747  _darf_journal_lesen
 26353-26373  _db_maintenance_loop
  6801-6829   _db_vacuum_loop
 18527-18551  _detect_foreign_ad
  1364-1375   _diag_path_owner
 19922-19966  _director_finalize
 20733-20740  _director_for
 19871-19919  _director_mark
 27349-27384  _disc_automod_check
 27322-27328  _disc_state_get
 27331-27338  _disc_state_set
 24393-24406  _discord_guild_filesize_bytes
 24592-24601  _discord_invite
 27283-27319  _discord_live_thread
 20073-20085  _discord_notify
 24493-24518  _discord_ops_alert
 27181-27279  _discord_post_user
 24657-26338  _discord_run_once
 24531-24589  _discord_start
 26870-26876  _discord_stop
 24414-24416  _discord_upload_limit_label
 24409-24411  _discord_upload_limit_mb
  6860-6934   _disk_alarm_loop
 29370-29419  _disk_autoclean
 29422-29435  _disk_guard_loop
 29362-29367  _disk_pct
 16321-16323  _drawtext_chain
 14638-14640  _dump_all_threads
 11458-11522  _enrich_proxies_with_geo
  2023-2067   _ensure_cookie_file_netscape
 24604-24654  _ensure_discord_invite
 27076-27108  _ensure_error_channel
  8648-8651   _ensure_notify_topic
 11701-11738  _ensure_proxy_ready
  8602-8629   _ensure_topic
   646-648    _env_int
   651-653    _env_int_range
 27148-27178  _error_channel_loop
 20117-20130  _event_webhook
 15773-15783  _evolution_loop
  5951-5985   _extract_file_payload
  2155-2157   _extract_urls_from_streamurl_node
 23715-23722  _f2b_sudo_hint
 20153-20155  _faster_whisper_available
 18416-18428  _fetch_ldnoobw_de
 11347-11365  _fetch_proxy_list
 20567-20595  _fetch_tiktok_room_id
   717-720    _ff_cmd
 16484-16489  _find_chromium
  3126-3130   _find_external_recorder
  2160-2162   _find_stream_urls
 15150-15175  _fire_webhooks
  7715-7724   _fork_safe
   798-807    _freeai_chat_sync_metered
 23765-23807  _geo_lookup_ips
  3582-3591   _get_ai_session
  7549-7589   _get_live_info
  2696-2703   _get_resolve_semaphore
  7950-8316   _handle_single_tracking
 29214-29216  _hb
 29219-29236  _hb_while
 16022-16024  _highlight_cfg
 16027-16056  _highlight_observe
 16492-16497  _htmlov_screenshot_cmd
 20311-20321  _httpx_proxy
 15183-15195  _in_quiet_hours
 30249-30280  _install_fast_eventloop
 10004-10058  _install_fast_json
 14643-14659  _install_faulthandler
 21426-21435  _intel_ensure_schema
 21473-21508  _intel_index_loop
 21447-21457  _intel_index_one
 21438-21444  _intel_semantic
  5320-5329   _is_authorized
  7880-7886   _is_dead
  2145-2147   _is_hevc
 23750-23756  _is_private_ip
  1528-1535   _is_process_running
  6539-6550   _is_quiet_hours
  1165-1174   _is_upload_window
 10093-10106  _json_error_handler
  6759-6789   _kick_broadcaster_id
 12031-12050  _kick_channel_live
  6673-6715   _kick_follower_count
 13194-13207  _kick_oauth_exchange
 13210-13212  _kick_oauth_page
 13153-13157  _kick_redirect_public
 13148-13150  _kick_redirect_source
 13140-13145  _kick_redirect_uri
  6658-6660   _kick_slug
 13160-13191  _kick_user_token
  3952-3955   _kind_from_filename
 15212-15217  _latest_popularity
 18438-18444  _learned_load
 18435-18436  _learned_path
 18446-18454  _learned_save
 20948-20978  _live_react_loop
 20744-20937  _live_react_worker
 19534-19545  _live_transcript_push
 20939-20946  _live_users
 19969-20013  _living_title_loop
 18395-18403  _load_banned_words_file
  1704-1777   _load_cookies_dict
 26551-26623  _local_backup_scan
 10075-10089  _log_5xx
 16907-16919  _looks_like_codec_err
 16902-16904  _looks_like_source_expired
  7796-7826   _loop_fehler
 14663-14672  _loop_heartbeat
 29184-29211  _loop_lag_monitor
 14782-14785  _loop_not_ready
 14675-14743  _loop_watchdog_thread
 19414-19428  _loyalty_add
 19405-19411  _loyalty_get
 19431-19439  _loyalty_top
 15349-15351  _manual_donations_total
  7888-7889   _mark_dead
 12198-12227  _marketing_cfg
 12189-12195  _marketing_default_targets
 12184-12186  _marketing_enabled
 12241-12256  _marketing_flavor
 12311-12327  _marketing_loop
 12259-12269  _marketing_post_discord
 12272-12284  _marketing_post_telegram
 12287-12308  _marketing_publish
 12230-12234  _marketing_state_obj
 12237-12238  _marketing_state_save
 27882-27900  _maybe_handle_command
 29521-29545  _maybe_hype_clip
  3870-3893   _migrate_columns
 28159-28170  _mod_is_exempt
 28173-28178  _mod_warn_first
 28181-28184  _mod_warn_text
 15810-15818  _modlog
   918-920    _multistream_targets
  7727-7728   _nc_create_subprocess_exec
  7731-7732   _nc_create_subprocess_shell
 12663-12680  _news_absaetze
 12422-12438  _news_cfg
 12409-12411  _news_enabled
 12476-12573  _news_facts
 12714-12736  _news_generate
 12921-12938  _news_loop
 12414-12419  _news_output_path
 12576-12578  _news_phrase
 12683-12711  _news_phrase_impl
 12451-12458  _news_read
 12441-12444  _news_state_obj
 12447-12448  _news_state_save
 12461-12473  _news_write
 15848-15850  _normalize_ingest
  2337-2354   _note_check_duration
  8642-8645   _notify_topic_name
 13104-13115  _oauth_redirect_env
 13131-13137  _oauth_redirect_source
 13118-13128  _oauth_redirect_uri
 19560-19568  _oracle_memories
 19826-19860  _oracle_memorize
 19571-19584  _oracle_persona
 19553-19557  _oracle_recent_text
 16147-16155  _ov_atomic_write
 16135-16141  _ov_bar
 18351-18363  _ov_clip_text
 16144-16145  _ov_oneline
 22934-22963  _overlay_push
 16438-16481  _overlay_render_size
 15909-15913  _overlay_session_reset
 22886-22889  _overlay_src_ok
 18514-18524  _own_invites
 16433-16435  _parse_size
 23958-24038  _parse_ssh_attacks
  7151-7184   _pause_resume_cmd
  1832-1876   _persist_refreshed_cookies
  1670-1702   _pick_checked_pull_proxy
 10174-10187  _pin_auth_value
 10233-10234  _pin_clear_fail
 10213-10216  _pin_locked
 10219-10230  _pin_note_fail
 10190-10210  _pin_ok
 22776-22778  _piper_available
 22741-22763  _piper_list_voices
 22783-22808  _piper_pick_model
 22820-22867  _piper_say
 22734-22738  _piper_voice_roots
 15112-15147  _post_json_threaded
 16412-16430  _probe_video_size
  1556-1573   _proc_is_recorder
 11445-11456  _proxy_geo_cache_put
 11672-11698  _proxy_pool_refresh_loop
  1636-1667   _proxy_report_recording
 14628-14630  _prune_stall_dumps
 13063-13101  _public_base_url
 12739-12860  _public_stats
 20088-20114  _push_notify
 10335-10337  _pwa_dir
 11416-11431  _quick_validate_proxy
 15178-15180  _quiet_hours_config
 10300-10333  _rate_guard
 19379-19385  _react_warn
  7635-7674   _reap_proc
  2377-2399   _record_check_outcome
   712-714    _redact_stream_urls
 11599-11669  _refresh_proxy_pool
 22766-22772  _resolve_piper_model
 14016-14031  _resolve_tracked_user
  2171-2261   _resolve_via_html
  2519-2673   _resolve_via_webcast_api_v2
  2736-2798   _resolve_via_ytdlp
 27501-27630  _resolve_youtube_ingest
 21017-21024  _restream_active_platforms
 15894-15905  _restream_active_sources
 20598-20697  _restream_chat_guardian
 16059-16131  _restream_chat_push
 15821-15833  _restream_enabled
 16500-16587  _restream_html_overlay_start
 16590-16603  _restream_html_overlay_stop
  1113-1115   _restream_layout_mode
 15859-15882  _restream_overlay_files
 20982-21014  _restream_platform_state
 21145-21180  _restream_resume_after_restart
 16651-16709  _restream_tts_enqueue_wav
 16374-16406  _restream_tts_feeder
 16371-16372  _restream_tts_fifo_path
 16606-16633  _restream_tts_start
 16635-16649  _restream_tts_stop
 21027-21142  _restream_verify_loop
 26516-26528  _retention_loop
 26475-26513  _retention_scan
  2481-2483   _room_is_abo
  5989-6106   _run_ai_call
 14766-14779  _run_async_from_flask
 23759-23762  _run_priv
 30237-30245  _run_selfcheck_and_exit
 26531-26542  _s3_client
  7891-7937   _safe_send
  4584-4600   _sample_net_throughput
 18405-18413  _save_banned_words_file
  2429-2456   _schedule_next_check
 26429-26472  _scheduler_loop
  3896-3900   _schema_pk
 14787-14792  _scraper_session
 28187-28226  _screen_full
 13520-13557  _sec_headers
  2150-2152   _select_stream_from_data_section
 30050-30234  _selfcheck
  8654-8688   _send_live_notice
  1188-1192   _should_defer_upload
 26942-26977  _shrink_for_discord
 10340-10352  _sicheres_ziel
 29442-29459  _sign_health_check
 29462-29481  _sign_health_loop
  7744-7755   _spawn
  7758-7788   _spawn_from_flask
 24082-24085  _st_befund
 20323-20564  _start_chat_listener
 14746-14763  _start_loop_watchdog
 12884-12912  _stats_loop
 12863-12866  _stats_output_path
 12869-12881  _stats_write
  8384-8398   _storage_cleanup_loop
 29501-29508  _story_for
  3188-3194   _stream_url_expiry
  3203-3209   _stream_url_is_fresh
  3196-3201   _stream_url_ttl
 18478-18485  _streamer_persona_get
 18460-18466  _streamer_personas_load
 18457-18458  _streamer_personas_path
 18468-18476  _streamer_personas_save
 16326-16330  _studio_chain
 26648-26770  _system_backup
 26773-26801  _system_backup_loop
 11368-11407  _test_proxy
 12072-12081  _testpush_cfg
 12084-12101  _testpush_exec
 12053-12069  _testpush_resolve_live
  8561-8571   _tg_topics_load_into_mem
  8558-8559   _tg_topics_path
  8573-8580   _tg_topics_save
 23400-23448  _tiktok_account_exists
 10148-10156  _token_ok
  8583-8587   _topic_forget
 15198-15209  _tracking_max_duration
  4202-4214   _tracking_resume_cleanup
  1422-1445   _try_attach_file_handler
 22810-22818  _tts_cleanup
 12009-12013  _tunnel_effective
 22236-22289  _twitch_channel_status
 28229-28372  _twitch_chat_loop
 28043-28146  _twitch_eventsub_loop
 15679-15682  _twitch_oauth_page
  1211-1224   _upload_queue_add
  1235-1237   _upload_queue_count
  1194-1203   _upload_queue_load
  1184-1186   _upload_queue_path
  1226-1233   _upload_queue_remove
  1205-1209   _upload_queue_save
  1239-1280   _upload_window_loop
  7608-7615   _uptime_s
 15836-15845  _url_host
   692-709    _url_ohne_zugang
   776-780    _usage_record_claude
  7829-7873   _verbindung_verloren
  6718-6749   _viewer_sample_loop
  6791-6798   _viewer_stats
 10237-10240  _wants_html
  7618-7632   _warn_empty_env
 29257-29352  _watchdog_loop
 27784-27792  _wchat_thank_ok
 20157-20187  _whisper_get_model
  7705-7712   _whisper_native_section
 19366-19372  _whisper_pool
 20256-20285  _whisper_segments
 20189-20253  _whisper_transcribe
 16157-16319  _write_restream_overlay
 28400-28479  _youtube_api_chat_loop
 22292-22395  _youtube_api_status
 22398-22465  _youtube_channel_status
 28482-28642  _youtube_chat_loop
 27636-27649  _youtube_restream_autoconfig
 27652-27676  _youtube_restream_autoconfig_inner
 27742-27770  _youtube_send
 22570-22611  _youtube_set_channel
 27679-27713  _yt_access_token
 27716-27731  _yt_live_chat_id
 28393-28397  _yt_oauth_configured
 27737-27739  _yt_sendrate_cfg
 28375-28390  _yt_timeout
  2720-2721   _ytdlp_detect_available
  2723-2734   _ytdlp_note_result
 14633-14635  _zombie_child_count
  7485-7509   about
  4071-4075   add_ai_log_entry
  3988-3991   add_archive_entry
  4697-4712   add_archive_rule
  4373-4407   add_recording
  4136-4153   add_tracking
  6109-6142   ai
  3735-3774   ai_chat
  3808-3818   ai_history_append
  3820-3825   ai_history_clear
  3797-3806   ai_history_load
  3782-3795   ai_rate_limit_check
  6171-6179   aireset
 19697-19716  azrael_chat
 28647-28769  brain_cmd
  3212-3396   build_recording_cmd
  4156-4159   bulk_add_trackings
  6982-7041   bulkadd
  8401-8541   check_all_trackings
  4218-4230   claim_live_transition
 18554-19309  class KickModerator
 16922-18238  class RestreamManager
 11783-11825  classify_proxy_anonymity
  6217-6415   cleanup
  5180-5221   cleanup_old_recordings
  4364-4371   clear_recording
 27387-27452  clip_moment
  4528-4577   compute_storage_forecast
  7104-7148   cookies_cmd
  4127-4133   count_trackings_for_chat
  4058-4069   decide_preferred_recorder
  3998-4001   delete_archive_entry
  4714-4722   delete_archive_rule
  5646-5793   diag
 28881-28942  einnahmen_cmd
  4522-4525   find_recordings_by_fingerprint
  4019-4035   finish_recording_attempt
  4190-4192   get_all_active_trackings
  4086-4089   get_all_checks
  4409-4412   get_all_recordings
  4471-4473   get_all_tags_with_counts
  4499-4502   get_annotations_for_recording
  3993-3996   get_archive_entry
  4492-4495   get_bookmarked_recordings
  1899-2016   get_cookie_health
  4459-4465   get_event_log
  4042-4056   get_last_recording_attempt
  2801-2906   get_live_status
  4980-4983   get_manual_recordings
  4507-4510   get_or_compute_inspect_sync
  5256-5300   get_outcome_breakdown
  4478-4481   get_priority_poll_interval
  4675-4684   get_profile_snapshots
  4037-4040   get_recent_recording_attempts
  4414-4417   get_recording_by_id
  4485-4488   get_recording_note
  3530-3553   get_redis
  4116-4119   get_stats
  5147-5178   get_storage_stats
  4815-4817   get_tiktok_status_distribution
  4232-4241   get_tracking_state
  4187-4188   get_trackings_for_group
  4996-4999   get_trash_recordings
  9309-9972   handle_recording_finished
  3918-3943   init_db
  5070-5124   inspect_stream_url
 22929-22931  is_revenue_platform
  4687-4695   list_archive_rules
  5450-5488   live
  7940-7948   live_check_worker
  3605-3639   llm_chat
  3662-3690   llm_chat_sync
  3647-3659   llm_list_models
  4425-4451   log_event
  1490-1523   log_recording_failure
  7298-7347   logs_cmd
 29549-30040  main
  6145-6168   on_ai_media
  7424-7450   on_ai_reply
  7453-7482   on_azrael_mention
  7514-7544   on_callback
 19719-19823  oracle_handle
  7187-7190   pause_tracking
  5310-5315   profile_keyboard
  7249-7295   quota
  8318-8381   reaper_loop
  4811-4813   record_tiktok_status
  6184-6214   recstatus
  3555-3563   redis_get_json
  3565-3571   redis_set_json
  4161-4185   remove_tracking
 28945-28955  report_cmd
 11828-11830  report_proxy_result
  2264-2291   resolve_tiktok_live_stream
  4991-4994   restore_recording
  7193-7196   resume_tracking
  4725-4805   run_archive_rules
 28958-29164  run_bot
 14555-14602  run_flask
  4603-4648   sample_bandwidth_for_active
  4654-4673   save_profile_snapshot
  4078-4084   save_tiktok_check
  4356-4362   set_recording_file
  4195-4199   set_tracking_paused
  4986-4989   soft_delete_recording
  8694-9307   split_and_send_video
  5363-5405   start
  4003-4017   start_recording_attempt
  6418-6456   stats
  4961-4978   stop_manual_recording
  7199-7246   stoprec
  6643-6651   summary_cmd
  7350-7421   sysres
  5795-5939   teststream
  5407-5448   tiktok
  7044-7101   topusers
  5525-5582   track
  5490-5522   track_exact
  5596-5644   tracklist
  4827-4959   trigger_manual_recording
  4317-4354   try_acquire_recording_lock
  5002-5061   universal_search
  5584-5594   untrack
 28772-28878  update_cmd
  4517-4520   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           class MarketingConfig, class MarketingState, compose, has_content, next_due_ts, should_post, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                build_items, class NewsConfig, class NewsState, item_id, merge, render_json, should_generate
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       looks_like_source_expired, normalize_ingest
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
trackingdb.py          add_tracking_tag, bulk_add_trackings, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking_tag, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                —
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
