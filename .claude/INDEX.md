# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (203)

```
 10417  GET              /                                                dashboard
 14935  GET              /api/abo/status                                  api_abo_status
 10490  GET              /api/active-recordings                           api_active_recordings
 15006  GET              /api/activity-pulse                              api_activity_pulse
 14813  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 22195  GET/POST         /api/audio/config                                api_audio_config
 22225  POST             /api/audio/testtone                              api_audio_testtone
 14879  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14903  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14907  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11942  GET              /api/automation/status                           api_automation_status
 11964  POST             /api/automation/toggle                           api_automation_toggle
 13740  GET              /api/azrael/agents                               api_azrael_agents
 11834  POST             /api/azrael/ask                                  api_azrael_ask
 22431  GET/POST         /api/azrael/context                              api_azrael_context
 13415  GET              /api/azrael/core                                 api_azrael_core
 22565  POST             /api/azrael/live_pause                           api_azrael_live_pause
 22555  GET              /api/azrael/live_status                          api_azrael_live_status
 22573  POST             /api/azrael/live_test                            api_azrael_live_test
 13749  GET              /api/azrael/memories                             api_azrael_memories
 22621  POST             /api/azrael/persona                              api_azrael_persona_set
 22612  GET              /api/azrael/personas                             api_azrael_personas
 22649  GET              /api/azrael/piper_status                         api_azrael_piper_status
 22404  POST             /api/azrael/react                                api_azrael_react
 22440  GET              /api/azrael/reaction                             api_azrael_reaction
 22592  GET              /api/azrael/reactions                            api_azrael_reactions
 22642  GET              /api/azrael/transcript                           api_azrael_transcript
 22527  POST             /api/azrael/tts_test                             api_azrael_tts_test
 22502  GET              /api/azrael/voices                               api_azrael_voices
 22666  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10789  GET              /api/backoff-watch                               api_backoff_watch
 14290  POST             /api/backup/run                                  api_backup_run
 14256  GET              /api/backup/status                               api_backup_status
 14245  POST             /api/backup/system                               api_backup_system
 14845  GET              /api/bandwidth/live                              api_bandwidth_live
 14798  GET              /api/bookmarks                                   api_bookmarks_list
 11052  GET              /api/brain                                       api_brain
 10989  GET              /api/brain/alarms                                api_brain_alarms
 10974  GET              /api/brain/creator                               api_brain_creator
 10951  GET              /api/brain/graph                                 api_brain_graph
 11012  GET              /api/brain/growth                                api_brain_growth
  9971  GET              /api/brain/health                                api_brain_health
 23147  GET              /api/channel/categories                          api_channel_categories
 23153  POST             /api/channel/set                                 api_channel_set
 22963  GET              /api/channels/status                             api_channels_status
 21839  POST             /api/chat/send                                   api_chat_send
 13944  GET              /api/chat/send_status                            api_chat_send_status
 10471  GET              /api/checks                                      api_checks
 22468  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 22451  GET              /api/clips                                       api_clips
 22484  POST/DELETE      /api/clips/clear                                 api_clips_clear
 22117  GET              /api/cohost                                      api_cohost
 22129  POST             /api/cohost/config                               api_cohost_config
 15314  GET              /api/community/stats                             api_community_stats
 24018  GET              /api/data/export                                 api_data_export
 22043  GET              /api/debug/threads                               api_debug_threads
 24845  GET              /api/defense/attacks                             api_defense_attacks
 24812  GET              /api/defense/crowdsec                            api_defense_crowdsec
 24830  GET              /api/defense/fail2ban                            api_defense_fail2ban
 24536  GET              /api/defense/overview                            api_defense_overview
 14352  POST             /api/discord/announce                            api_discord_announce
 14080  GET              /api/discord/clips_week                          api_discord_clips_week
 14296  GET              /api/discord/community                           api_discord_community
 13972  GET              /api/discord/invite                              api_discord_invite
 13546  GET              /api/discord/overview                            api_discord_overview
 13632  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14827  GET              /api/events                                      api_events
 14127  GET              /api/events/stream                               api_events_stream
 16261  GET              /api/evolution/changelog                         api_evolution_changelog
 16246  GET              /api/evolution/history                           api_evolution_history
 16186  GET              /api/evolution/learned                           api_evolution_learned
 16208  GET              /api/evolution/proposals                         api_evolution_proposals
 16229  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss
 16176  POST             /api/evolution/run                               api_evolution_run
 16276  GET              /api/evolution/snapshots                         api_evolution_snapshots
 16141  GET              /api/evolution/status                            api_evolution_status
 14840  GET              /api/forecast/storage                            api_forecast_storage
 11980  GET              /api/freeai/status                               api_freeai_status
 13488  GET              /api/health                                      api_health
 14858  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14854  GET              /api/heatmap/recordings                          api_heatmap_recordings
 22166  GET              /api/highlights                                  api_highlights
 22178  POST             /api/highlights/config                           api_highlights_config
 23004  GET              /api/kick/channel                                api_kick_channel
 23025  POST             /api/kick/channel                                api_kick_channel_set
 13215  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 13283  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 13261  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 13200  GET              /api/kick/oauth/start                            api_kick_oauth_start
 13240  GET              /api/kick/oauth/status                           api_kick_oauth_status
 22243  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 22312  POST             /api/kickmod/config                              api_kickmod_config
 22357  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 22371  GET              /api/kickmod/learned                             api_kickmod_learned
 22398  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 22378  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 22709  POST             /api/kickmod/say                                 api_kickmod_say
 22685  POST             /api/kickmod/start                               api_kickmod_start
 22283  GET              /api/kickmod/status                              api_kickmod_status
 22696  POST             /api/kickmod/stop                                api_kickmod_stop
 10351  POST             /api/login                                       dashboard_login_submit
 15299  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12343  POST             /api/marketing/config                            api_marketing_config
 12368  GET              /api/marketing/preview                           api_marketing_preview
 12378  POST             /api/marketing/send-now                          api_marketing_send_now
 12317  GET              /api/marketing/status                            api_marketing_status
 12335  POST             /api/marketing/toggle                            api_marketing_toggle
 12979  POST             /api/news/config                                 api_news_config
 12945  GET              /api/news/creators                               api_news_creators
 12956  POST             /api/news/creators/generate                      api_news_creators_generate
 13021  POST             /api/news/generate-now                           api_news_generate_now
 13016  GET              /api/news/items                                  api_news_items
 13007  GET              /api/news/preview                                api_news_preview
 12926  GET              /api/news/status                                 api_news_status
 12971  POST             /api/news/toggle                                 api_news_toggle
 15268  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13909  GET              /api/notify/status                               api_notify_status
 13920  POST             /api/notify/test                                 api_notify_test
 10575  GET              /api/outcomes                                    api_outcomes
 23624  POST             /api/overlay/config                              api_overlay_config
 23611  POST             /api/overlay/event                               api_overlay_event
 23516  GET              /api/overlay/state                               api_overlay_state
 10608  GET              /api/profile/<username>                          api_profile
 15024  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14866  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14989  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14966  GET              /api/proxy/trend                                 api_proxy_trend
 12900  GET              /api/public/stats                                api_public_stats
 10451  GET              /api/pulse                                       api_pulse
 14430  GET              /api/recording-attempts                          api_recording_attempts
 21774  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 21752  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 21793  POST             /api/restream/<int:rid>/start                    api_restream_start
 22064  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 23478  GET              /api/restream/chatfeed                           api_restream_chatfeed
 21728  POST             /api/restream/create                             api_restream_create
 13291  GET              /api/restream/deck                               api_restream_deck
 11916  GET              /api/restream/health                             api_restream_health
 23500  POST             /api/restream/layout                             api_restream_layout
 21701  GET              /api/restream/list                               api_restream_list
 11885  POST             /api/restream/report                             api_restream_report
 22077  POST             /api/restream/start_all                          api_restream_start_all
 22103  POST             /api/restream/stop_all                           api_restream_stop_all
 12091  GET              /api/restream/testpush                           api_testpush_status
 12116  POST             /api/restream/testpush                           api_testpush_run
 15399  GET              /api/restream/verify                             api_restream_verify
 14058  GET              /api/retention/preview                           api_retention_preview
 14067  POST             /api/retention/run                               api_retention_run
 14783  GET              /api/search                                      api_search
 24583  GET              /api/selftest                                    api_selftest
 21810  GET              /api/shield/stats                                api_shield_stats
 10512  GET              /api/storage                                     api_storage
 10519  POST             /api/storage/cleanup                             api_storage_cleanup
 14920  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11855  GET              /api/stream/timeline                             api_stream_timeline
 13620  GET              /api/stream/transcript                           api_stream_transcript
 23766  GET              /api/streamer/compare                            api_streamer_compare
 23965  POST             /api/streamer/delete/<username>                  api_streamer_delete
 14019  GET              /api/streamer/detail                             api_streamer_detail
 23990  GET              /api/streamer/digest/<username>                  api_streamer_digest
 23870  GET              /api/streamer/dormant                            api_streamer_dormant
 23946  GET              /api/streamer/exists/<username>                  api_streamer_exists
 23825  GET              /api/streamer/journal/<username>                 api_streamer_journal
 23790  GET/POST         /api/streamer/priority/<username>                api_streamer_priority
 23850  GET              /api/streamer/watchlist                          api_streamer_watchlist
 13455  GET              /api/streamers/wall                              api_streamers_wall
 10543  GET              /api/summary/preview                             api_summary_preview
 14495  GET              /api/system                                      api_system
 15347  GET              /api/system/check_timing                         api_check_timing
 15670  GET              /api/system/config_drift                         api_config_drift
 13656  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13767  GET              /api/system/preflight                            api_system_preflight
 13893  GET              /api/system/preflight_history                    api_system_preflight_history
 14192  GET              /api/system/resilience                           api_system_resilience
 14818  GET              /api/tags                                        api_tags_list
 10485  GET              /api/top                                         api_top
 10844  GET              /api/trend-7d                                    api_trend_7d
 22516  GET              /api/tts/<fn>                                    api_tts_file
 15642  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback
 15594  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect
 15618  GET              /api/twitch/oauth/start                          api_twitch_oauth_start
 15572  GET              /api/twitch/oauth/status                         api_twitch_oauth_status
 23652  GET              /api/upload_window                               api_upload_window
 10589  GET              /api/userstats                                   api_userstats
 13032  GET              /api/version                                     api_version
 15493  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback
 15514  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget
 15526  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout
 15451  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect
 15475  GET              /api/youtube/oauth/start                         api_youtube_oauth_start
 15429  GET              /api/youtube/oauth/status                        api_youtube_oauth_status
 28265  GET              /api/youtube/sendrate                            api_youtube_sendrate
 14468  GET              /archive/<int:eid>/download                      archive_download
 14525  GET              /download/<int:recording_id>                     download
 14408  GET              /health                                          health
 22012  GET              /healthz                                         healthz
 10342  GET              /login                                           dashboard_login_page
 10372  GET              /logout                                          dashboard_logout
 10379  GET              /manifest.webmanifest                            pwa_manifest
 13684  GET              /metrics                                         api_prometheus_metrics
 23461  GET              /overlay                                         overlay_page
 10403  GET              /pwa-icon-<variant>.png                          pwa_icon
 10389  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (152)

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
 25288  /ai                     AZRAEL / KI fragen (Text oder Sprachnachricht)
 25747  /ask                    AZRAEL etwas fragen — der KI-Community-Assistent
 25379  /assign_role            Rolle/Gruppe einem Mitglied geben
 25425  /ban                    Mitglied bannen
 26079  /botstats               Bot-Health: Uptime, Trackings, Aufnahmen, DB (Admin)
 26003  /clearwarns             Alle Verwarnungen eines Mitglieds löschen
 26043  /clip                   Highlight-Clip der letzten Sekunden vom laufenden Stream
 26028  /clipoftheweek          Aktuell führender Clip-of-the-Week (⭐-Voting)
 25870  /clips                  Letzte Highlight-Clips eines Users
 25340  /create_category        Kategorie anlegen
 25309  /create_channel         Text-Channel anlegen (optional in Kategorie)
 25368  /create_group           Nutzergruppe (= Rolle) anlegen
 25351  /create_role            Rolle / Nutzergruppe anlegen
 25325  /create_voice           Voice-Channel anlegen
 25661  /daily                  Tägliche XP-Belohnung abholen (Streak-Bonus!)
 25777  /event                  Community-Event ankündigen (Admin) — mit Countdown
 25820  /events                 Kommende Community-Events anzeigen
 25916  /follow                 Bei Live-Gang eines Streamers gepingt werden
 25900  /help                   Alle Bot-Befehle anzeigen
 25414  /kick                   Mitglied kicken
 25643  /leaderboard            Top-10 der Community nach XP
 25856  /livenow                Welche getrackten User sind gerade live
 25886  /post_test              Test: Nachricht in den Channel eines getrackten Users posten
 25717  /profile                Dein Community-Profil: Level, Rang, Streak, Rang-Platz
 25449  /purge                  Letzte N Nachrichten im Channel löschen (max 100)
 25629  /rank                   Dein Level und Rang anzeigen
 25843  /recstatus              Aktuell laufende Aufnahmen
 25390  /remove_role            Rolle/Gruppe entfernen
 25302  /restream_status        Restream-Status
 25401  /set_channel_perms      Rechte einer Rolle für einen Channel setzen
 25594  /setup_community        Community-Server einrichten: Ränge, Channels, Rechte
 25612  /setup_targets          Pro getracktem User: Clips-, Chat- und Voice-Channel anlegen
 25942  /stats                  Statistik zu einem getrackten Streamer
 25214  /status                 Azrael Sentinel Status: Trackings, Live, Restream
 26238  /streaminfo             Kompakt-Karte eines Streamers: Aktivität, Aufnahmen, Followe
 26135  /sys_report             Azrael Sentinel Wochenreport (Brain, Markdown)
 26111  /sys_unpause            Auto-pausierte Quelle wieder aktivieren (Admin)
 25436  /timeout                Mitglied stummschalten (Minuten)
 26014  /topstreamers           Rangliste der Streamer nach Aufnahmen
 25244  /track                  TikTok-User tracken
 25228  /tracklist              Getrackte TikTok-User dieses Servers
 25931  /unfollow               Live-Pings für einen Streamer abbestellen
 25277  /untrack                TikTok-User nicht mehr tracken
 25964  /warn                   Mitglied verwarnen (eskaliert ab 3 Verwarnungen zu Timeout)
 25988  /warnings               Verwarnungen eines Mitglieds anzeigen
```

## Discord-Events (4)

```
 26722  on_member_join
 26684  on_message
 26325  on_raw_reaction_add
 26757  on_ready
```

## Top-Level-Symbole in bot.py (553 Funktionen, 2 Klassen)

```
  2474-2475   _abo_key
  2495-2513   _abo_probe_dump
 24125-24135  _active_recorder_sync
 18998-19005  _ad_allowlist
 20120-20126  _agent_for
 24137-24155  _ai_calls_total_sync
 20129-20145  _ai_telemetry
 20627-20645  _alert
 26870-26920  _alert_monitor_loop
 27296-27358  _announce_loop
  3416-3419   _anthropic_key
  3426-3428   _anthropic_model
 10099-10102  _arg_int
  2466-2471   _as_dict
 16858-16863  _audio_cfg
 20781-20803  _audio_tap_cmd
 10263-10274  _auth_cookie
 10230-10259  _auth_guard
  1622-1627   _auto_on
 21677-21695  _auto_restream_loop
 28426-28441  _azrael_broadcast_reply
 28326-28348  _azrael_chat_reply
 28309-28323  _azrael_chat_should_reply
 12599-12617  _azrael_creator_take
 28354-28356  _azrael_gate_cfg
 20150-20164  _azrael_live_state
 23364-23378  _azrael_overlay_state
 20510-20564  _azrael_proactive_loop
 19969-20025  _azrael_reaction_to_chats
 28359-28366  _azrael_reply_all_chats
 28296-28306  _azrael_self_names
 28394-28423  _azrael_send_to
 20167-20188  _azrael_system
 27036-27039  _backup_active
 27117-27130  _backup_loop
 18886-18887  _badwords_path
 26835-26844  _brain_growth_loop
 10920-10947  _brain_growth_snapshot
  2402-2422   _brain_hint_delay
 10912-10914  _brain_history_for
  6505-6533   _brain_notify
 10889-10910  _brain_record
 10916-10918  _brain_stream_recent
 14106-14123  _browser_push
  6549-6636   _build_daily_summary
  2905-3085   _build_native_cmd
 17206-17393  _build_restream_cmd
  3129-3162   _build_ytdlp_cmd
 24077-24084  _cached_probe
  5327-5354   _can_stop_tracking
  1802-1824   _capture_set_cookies
 15083-15086  _cfg_get
 15089-15091  _cfg_set
 23108-23143  _channel_set_all
 16456-16459  _chat_connected
 16462-16478  _chat_disconnected
  8579-8590   _chat_is_forum
 16498-16500  _chat_sanitize
 16502-16511  _chat_src_ok
 16441-16453  _chat_stat
 16481-16484  _chat_stats_snapshot
  3691-3702   _check_ai_alive_sync
  3705-3717   _check_ai_models_sync
 24086-24099  _check_redis_alive_sync
 24101-24121  _check_redis_version_sync
 13984-13997  _ci_key
 11519-11562  _classify_pool_anonymity
 11565-11582  _classify_pool_anonymity_bg
   782-786    _claude_chat_sync_metered
 10124-10131  _client_ip
 27390-27417  _clip_prune
 27420-27430  _clip_recfile_for
 27946-27952  _clip_should_velocity
 27471-27553  _clip_to_discord
  3589-3598   _close_ai_session
 28470-28485  _cohost_broadcast
 28452-28456  _cohost_cfg
 28511-28523  _cohost_fire_highlight
 28459-28467  _cohost_gate
 28488-28508  _cohost_highlight
 27602-27636  _community_events_loop
 10743-10745  _conv_messages
  6929-6969   _cookie_alarm_loop
  1874-1878   _cookie_autorefresh_info
  1779-1783   _cookie_header
 14156-14188  _cpu_load_snapshot
  3899-3911   _create_index_safe
 12567-12582  _creator_activity
 12623-12646  _creator_dossier_generate
 12585-12596  _creator_facts_line
 24338-24444  _crowdsec_status
 24304-24335  _crowdsec_via_lapi
 24169-24187  _cscli_bin
 24193-24206  _cscli_path
  6822-6847   _daily_summary_loop
 24224-24241  _darf_journal_lesen
 26847-26867  _db_maintenance_loop
  6794-6819   _db_vacuum_loop
 19021-19045  _detect_foreign_ad
  1360-1371   _diag_path_owner
 20416-20460  _director_finalize
 21227-21234  _director_for
 20365-20413  _director_mark
 27840-27875  _disc_automod_check
 27813-27819  _disc_state_get
 27822-27829  _disc_state_set
 24887-24900  _discord_guild_filesize_bytes
 25086-25095  _discord_invite
 27774-27810  _discord_live_thread
 20567-20579  _discord_notify
 24987-25012  _discord_ops_alert
 27672-27770  _discord_post_user
 25151-26832  _discord_run_once
 25025-25083  _discord_start
 27361-27367  _discord_stop
 24908-24910  _discord_upload_limit_label
 24903-24905  _discord_upload_limit_mb
  6850-6924   _disk_alarm_loop
 29852-29901  _disk_autoclean
 29904-29917  _disk_guard_loop
 29844-29849  _disk_pct
 16815-16817  _drawtext_chain
 14622-14624  _dump_all_threads
 11444-11508  _enrich_proxies_with_geo
  2019-2063   _ensure_cookie_file_netscape
 25098-25148  _ensure_discord_invite
 27567-27599  _ensure_error_channel
  8638-8641   _ensure_notify_topic
 11687-11724  _ensure_proxy_ready
  8592-8619   _ensure_topic
   645-647    _env_int
   650-652    _env_int_range
 27639-27669  _error_channel_loop
 20611-20624  _event_webhook
 15749-15755  _evo_build_dir
 15758-15765  _evo_version
 16041-16122  _evolution_cycle
 15774-15794  _evolution_llm_note
 16125-16135  _evolution_loop
 15797-16038  _evolution_write_build
  5947-5981   _extract_file_payload
  2151-2153   _extract_urls_from_streamurl_node
 24209-24216  _f2b_sudo_hint
 20647-20649  _faster_whisper_available
 18910-18922  _fetch_ldnoobw_de
 11333-11351  _fetch_proxy_list
 21061-21089  _fetch_tiktok_room_id
   716-719    _ff_cmd
 16978-16983  _find_chromium
  3122-3126   _find_external_recorder
  2156-2158   _find_stream_urls
 15134-15159  _fire_webhooks
  7705-7714   _fork_safe
   797-806    _freeai_chat_sync_metered
 24259-24301  _geo_lookup_ips
  3578-3587   _get_ai_session
  7539-7579   _get_live_info
  2692-2699   _get_resolve_semaphore
  7940-8306   _handle_single_tracking
 29696-29698  _hb
 29701-29718  _hb_while
 16516-16518  _highlight_cfg
 16521-16550  _highlight_observe
 16986-16991  _htmlov_screenshot_cmd
 20805-20815  _httpx_proxy
 15167-15179  _in_quiet_hours
 30731-30762  _install_fast_eventloop
  9994-10048  _install_fast_json
 14627-14643  _install_faulthandler
 21920-21929  _intel_ensure_schema
 21967-22002  _intel_index_loop
 21941-21951  _intel_index_one
 21932-21938  _intel_semantic
  5316-5325   _is_authorized
  7870-7876   _is_dead
  2141-2143   _is_hevc
 24244-24250  _is_private_ip
  1524-1531   _is_process_running
  6535-6546   _is_quiet_hours
  1164-1173   _is_upload_window
 10083-10096  _json_error_handler
  6752-6782   _kick_broadcaster_id
 12017-12036  _kick_channel_live
  6669-6711   _kick_follower_count
 13178-13191  _kick_oauth_exchange
 13194-13196  _kick_oauth_page
 13137-13141  _kick_redirect_public
 13132-13134  _kick_redirect_source
 13124-13129  _kick_redirect_uri
  6654-6656   _kick_slug
 13144-13175  _kick_user_token
  3948-3951   _kind_from_filename
 15196-15201  _latest_popularity
 18932-18938  _learned_load
 18929-18930  _learned_path
 18940-18948  _learned_save
 21442-21472  _live_react_loop
 21238-21431  _live_react_worker
 20028-20039  _live_transcript_push
 21433-21440  _live_users
 20463-20507  _living_title_loop
 18889-18897  _load_banned_words_file
  1700-1773   _load_cookies_dict
 27042-27114  _local_backup_scan
 10065-10079  _log_5xx
 17401-17413  _looks_like_codec_err
 17396-17398  _looks_like_source_expired
  7786-7816   _loop_fehler
 14647-14656  _loop_heartbeat
 29666-29693  _loop_lag_monitor
 14766-14769  _loop_not_ready
 14659-14727  _loop_watchdog_thread
 19908-19922  _loyalty_add
 19899-19905  _loyalty_get
 19925-19933  _loyalty_top
 15333-15335  _manual_donations_total
  7878-7879   _mark_dead
 12184-12213  _marketing_cfg
 12175-12181  _marketing_default_targets
 12170-12172  _marketing_enabled
 12227-12242  _marketing_flavor
 12297-12313  _marketing_loop
 12245-12255  _marketing_post_discord
 12258-12270  _marketing_post_telegram
 12273-12294  _marketing_publish
 12216-12220  _marketing_state_obj
 12223-12224  _marketing_state_save
 28373-28391  _maybe_handle_command
 30003-30027  _maybe_hype_clip
  3866-3889   _migrate_columns
 28650-28661  _mod_is_exempt
 28664-28669  _mod_warn_first
 28672-28675  _mod_warn_text
 16304-16312  _modlog
   917-919    _multistream_targets
  7717-7718   _nc_create_subprocess_exec
  7721-7722   _nc_create_subprocess_shell
 12649-12666  _news_absaetze
 12408-12424  _news_cfg
 12395-12397  _news_enabled
 12462-12559  _news_facts
 12700-12722  _news_generate
 12905-12922  _news_loop
 12400-12405  _news_output_path
 12562-12564  _news_phrase
 12669-12697  _news_phrase_impl
 12437-12444  _news_read
 12427-12430  _news_state_obj
 12433-12434  _news_state_save
 12447-12459  _news_write
 16342-16344  _normalize_ingest
  2333-2350   _note_check_duration
  8632-8635   _notify_topic_name
 13088-13099  _oauth_redirect_env
 13115-13121  _oauth_redirect_source
 13102-13112  _oauth_redirect_uri
 20054-20062  _oracle_memories
 20320-20354  _oracle_memorize
 20065-20078  _oracle_persona
 20047-20051  _oracle_recent_text
 16641-16649  _ov_atomic_write
 16629-16635  _ov_bar
 18845-18857  _ov_clip_text
 16638-16639  _ov_oneline
 23428-23457  _overlay_push
 16932-16975  _overlay_render_size
 16403-16407  _overlay_session_reset
 23380-23383  _overlay_src_ok
 19008-19018  _own_invites
 16927-16929  _parse_size
 24452-24532  _parse_ssh_attacks
  7141-7174   _pause_resume_cmd
  1828-1872   _persist_refreshed_cookies
  1666-1698   _pick_checked_pull_proxy
 10160-10173  _pin_auth_value
 10219-10220  _pin_clear_fail
 10199-10202  _pin_locked
 10205-10216  _pin_note_fail
 10176-10196  _pin_ok
 23270-23272  _piper_available
 23235-23257  _piper_list_voices
 23277-23302  _piper_pick_model
 23314-23361  _piper_say
 23228-23232  _piper_voice_roots
 15096-15131  _post_json_threaded
 16906-16924  _probe_video_size
  1552-1569   _proc_is_recorder
 11431-11442  _proxy_geo_cache_put
 11658-11684  _proxy_pool_refresh_loop
  1632-1663   _proxy_report_recording
 14612-14614  _prune_stall_dumps
 13047-13085  _public_base_url
 12725-12846  _public_stats
 20582-20608  _push_notify
 10321-10323  _pwa_dir
 11402-11417  _quick_validate_proxy
 15162-15164  _quiet_hours_config
 10286-10319  _rate_guard
 19873-19879  _react_warn
  7625-7664   _reap_proc
  2373-2395   _record_check_outcome
   711-713    _redact_stream_urls
 11585-11655  _refresh_proxy_pool
 23260-23266  _resolve_piper_model
 14000-14015  _resolve_tracked_user
  2167-2257   _resolve_via_html
  2515-2669   _resolve_via_webcast_api_v2
  2732-2794   _resolve_via_ytdlp
 27992-28121  _resolve_youtube_ingest
 21511-21518  _restream_active_platforms
 16388-16399  _restream_active_sources
 21092-21191  _restream_chat_guardian
 16553-16625  _restream_chat_push
 16315-16327  _restream_enabled
 16994-17081  _restream_html_overlay_start
 17084-17097  _restream_html_overlay_stop
  1112-1114   _restream_layout_mode
 16353-16376  _restream_overlay_files
 21476-21508  _restream_platform_state
 21639-21674  _restream_resume_after_restart
 17145-17203  _restream_tts_enqueue_wav
 16868-16900  _restream_tts_feeder
 16865-16866  _restream_tts_fifo_path
 17100-17127  _restream_tts_start
 17129-17143  _restream_tts_stop
 21521-21636  _restream_verify_loop
 27007-27019  _retention_loop
 26966-27004  _retention_scan
  2477-2479   _room_is_abo
  5985-6102   _run_ai_call
 14750-14763  _run_async_from_flask
 24253-24256  _run_priv
 30719-30727  _run_selfcheck_and_exit
 27022-27033  _s3_client
  7881-7927   _safe_send
  4580-4596   _sample_net_throughput
 18899-18907  _save_banned_words_file
  2425-2452   _schedule_next_check
 26923-26963  _scheduler_loop
  3892-3896   _schema_pk
 14771-14776  _scraper_session
 28678-28717  _screen_full
 13504-13541  _sec_headers
  2146-2148   _select_stream_from_data_section
 30532-30716  _selfcheck
  8644-8678   _send_live_notice
  1187-1191   _should_defer_upload
 27433-27468  _shrink_for_discord
 10326-10338  _sicheres_ziel
 29924-29941  _sign_health_check
 29944-29963  _sign_health_loop
  7734-7745   _spawn
  7748-7778   _spawn_from_flask
 24576-24579  _st_befund
 20817-21058  _start_chat_listener
 14730-14747  _start_loop_watchdog
 12870-12896  _stats_loop
 12849-12852  _stats_output_path
 12855-12867  _stats_write
  8374-8388   _storage_cleanup_loop
 29983-29990  _story_for
  3184-3190   _stream_url_expiry
  3199-3205   _stream_url_is_fresh
  3192-3197   _stream_url_ttl
 18972-18979  _streamer_persona_get
 18954-18960  _streamer_personas_load
 18951-18952  _streamer_personas_path
 18962-18970  _streamer_personas_save
 16820-16824  _studio_chain
 27139-27261  _system_backup
 27264-27292  _system_backup_loop
 11354-11393  _test_proxy
 12058-12067  _testpush_cfg
 12070-12087  _testpush_exec
 12039-12055  _testpush_resolve_live
  8551-8561   _tg_topics_load_into_mem
  8548-8549   _tg_topics_path
  8563-8570   _tg_topics_save
 23894-23942  _tiktok_account_exists
 10134-10142  _token_ok
  8573-8577   _topic_forget
 15182-15193  _tracking_max_duration
  4198-4210   _tracking_resume_cleanup
  1418-1441   _try_attach_file_handler
 23304-23312  _tts_cleanup
 11995-11999  _tunnel_effective
 22730-22783  _twitch_channel_status
 28720-28863  _twitch_chat_loop
 28534-28637  _twitch_eventsub_loop
 15663-15666  _twitch_oauth_page
  1210-1223   _upload_queue_add
  1234-1236   _upload_queue_count
  1193-1202   _upload_queue_load
  1183-1185   _upload_queue_path
  1225-1232   _upload_queue_remove
  1204-1208   _upload_queue_save
  1238-1276   _upload_window_loop
  7598-7605   _uptime_s
 16330-16339  _url_host
   691-708    _url_ohne_zugang
   775-779    _usage_record_claude
  7819-7863   _verbindung_verloren
  6714-6742   _viewer_sample_loop
  6784-6791   _viewer_stats
 10223-10226  _wants_html
  7608-7622   _warn_empty_env
 29739-29834  _watchdog_loop
 28275-28283  _wchat_thank_ok
 20651-20681  _whisper_get_model
  7695-7702   _whisper_native_section
 19860-19866  _whisper_pool
 20750-20779  _whisper_segments
 20683-20747  _whisper_transcribe
 16651-16813  _write_restream_overlay
 28891-28964  _youtube_api_chat_loop
 22786-22889  _youtube_api_status
 22892-22959  _youtube_channel_status
 28967-29124  _youtube_chat_loop
 28127-28140  _youtube_restream_autoconfig
 28143-28167  _youtube_restream_autoconfig_inner
 28233-28261  _youtube_send
 23064-23105  _youtube_set_channel
 28170-28204  _yt_access_token
 28207-28222  _yt_live_chat_id
 28884-28888  _yt_oauth_configured
 28228-28230  _yt_sendrate_cfg
 28866-28881  _yt_timeout
  2716-2717   _ytdlp_detect_available
  2719-2730   _ytdlp_note_result
 14617-14619  _zombie_child_count
  7475-7499   about
  4067-4071   add_ai_log_entry
  3984-3987   add_archive_entry
  4693-4708   add_archive_rule
  4369-4403   add_recording
  4132-4149   add_tracking
  6105-6138   ai
  3731-3770   ai_chat
  3804-3814   ai_history_append
  3816-3821   ai_history_clear
  3793-3802   ai_history_load
  3778-3791   ai_rate_limit_check
  6167-6175   aireset
 20191-20210  azrael_chat
 29129-29251  brain_cmd
  3208-3392   build_recording_cmd
  4152-4155   bulk_add_trackings
  6972-7031   bulkadd
  8391-8531   check_all_trackings
  4214-4226   claim_live_transition
 19048-19803  class KickModerator
 17416-18732  class RestreamManager
 11769-11811  classify_proxy_anonymity
  6213-6411   cleanup
  5176-5217   cleanup_old_recordings
  4360-4367   clear_recording
 27878-27943  clip_moment
  4524-4573   compute_storage_forecast
  7094-7138   cookies_cmd
  4123-4129   count_trackings_for_chat
  4054-4065   decide_preferred_recorder
  3994-3997   delete_archive_entry
  4710-4718   delete_archive_rule
  5642-5789   diag
 29363-29424  einnahmen_cmd
  4518-4521   find_recordings_by_fingerprint
  4015-4031   finish_recording_attempt
  4186-4188   get_all_active_trackings
  4082-4085   get_all_checks
  4405-4408   get_all_recordings
  4467-4469   get_all_tags_with_counts
  4495-4498   get_annotations_for_recording
  3989-3992   get_archive_entry
  4488-4491   get_bookmarked_recordings
  1895-2012   get_cookie_health
  4455-4461   get_event_log
  4038-4052   get_last_recording_attempt
  2797-2902   get_live_status
  4976-4979   get_manual_recordings
  4503-4506   get_or_compute_inspect_sync
  5252-5296   get_outcome_breakdown
  4474-4477   get_priority_poll_interval
  4671-4680   get_profile_snapshots
  4033-4036   get_recent_recording_attempts
  4410-4413   get_recording_by_id
  4481-4484   get_recording_note
  3526-3549   get_redis
  4112-4115   get_stats
  5143-5174   get_storage_stats
  4811-4813   get_tiktok_status_distribution
  4228-4237   get_tracking_state
  4183-4184   get_trackings_for_group
  4992-4995   get_trash_recordings
  9299-9962   handle_recording_finished
  3914-3939   init_db
  5066-5120   inspect_stream_url
 23423-23425  is_revenue_platform
  4683-4691   list_archive_rules
  5446-5484   live
  7930-7938   live_check_worker
  3601-3635   llm_chat
  3658-3686   llm_chat_sync
  3643-3655   llm_list_models
  4421-4447   log_event
  1486-1519   log_recording_failure
  7288-7337   logs_cmd
 30031-30522  main
  6141-6164   on_ai_media
  7414-7440   on_ai_reply
  7443-7472   on_azrael_mention
  7504-7534   on_callback
 20213-20317  oracle_handle
  7177-7180   pause_tracking
  5306-5311   profile_keyboard
  7239-7285   quota
  8308-8371   reaper_loop
  4807-4809   record_tiktok_status
  6180-6210   recstatus
  3551-3559   redis_get_json
  3561-3567   redis_set_json
  4157-4181   remove_tracking
 29427-29437  report_cmd
 11814-11816  report_proxy_result
  2260-2287   resolve_tiktok_live_stream
  4987-4990   restore_recording
  7183-7186   resume_tracking
  4721-4801   run_archive_rules
 29440-29646  run_bot
 14539-14586  run_flask
  4599-4644   sample_bandwidth_for_active
  4650-4669   save_profile_snapshot
  4074-4080   save_tiktok_check
  4352-4358   set_recording_file
  4191-4195   set_tracking_paused
  4982-4985   soft_delete_recording
  8684-9297   split_and_send_video
  5359-5401   start
  3999-4013   start_recording_attempt
  6414-6452   stats
  4957-4974   stop_manual_recording
  7189-7236   stoprec
  6639-6647   summary_cmd
  7340-7411   sysres
  5791-5935   teststream
  5403-5444   tiktok
  7034-7091   topusers
  5521-5578   track
  5486-5518   track_exact
  5592-5640   tracklist
  4823-4955   trigger_manual_recording
  4313-4350   try_acquire_recording_lock
  4998-5057   universal_search
  5580-5590   untrack
 29254-29360  update_cmd
  4513-4516   update_recording_fingerprint
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
evolution.py           analyze
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
